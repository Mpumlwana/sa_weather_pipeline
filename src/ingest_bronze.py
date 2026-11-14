"""Deliverable 1: load raw Open-Meteo history into the bronze Delta table.

Bronze keeps each API answer exactly as received. Nothing is edited.
A request window (source + city + start + end) already in bronze is skipped,
so running the script twice adds no duplicates.
"""
import csv
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import date, datetime, timedelta, timezone

from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType, TimestampType

import common

HISTORY_START = date(2025, 1, 1)
BRONZE_TABLE = str(common.BRONZE_DIR / "weather_raw")
PAUSE_SECONDS = 0.3

SCHEMA = StructType([
    StructField("batch_id", StringType(), False),
    StructField("ingested_at", TimestampType(), False),
    StructField("source", StringType(), False),
    StructField("city", StringType(), False),
    StructField("start_date", StringType(), False),
    StructField("end_date", StringType(), False),
    StructField("request_url", StringType(), False),
    StructField("http_status", IntegerType(), False),
    StructField("response_body", StringType(), True),
])


def read_cities():
    with open(common.CITIES_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def month_windows(first_day, last_day):
    """Yield (start, end) for every full calendar month from first_day up to last_day."""
    start = first_day
    while True:
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
        if end > last_day:
            return
        yield start, end
        start = next_month


def build_url(city, start, end):
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": ",".join(common.DAILY_VARIABLES),
        "timezone": common.TIMEZONE,
    }
    return common.ARCHIVE_URL + "?" + urllib.parse.urlencode(params)


def fetch(url):
    """Return (http_status, body). Retry three times on network problems."""
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return response.status, response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 * attempt)


def already_loaded(spark):
    """Return the (city, start, end) windows that bronze already holds with status 200."""
    if not DeltaTable.isDeltaTable(spark, BRONZE_TABLE):
        return set()
    rows = (
        spark.read.format("delta").load(BRONZE_TABLE)
        .where((F.col("http_status") == 200) & (F.col("source") == "archive"))
        .select("city", "start_date", "end_date")
        .collect()
    )
    return {(r.city, r.start_date, r.end_date) for r in rows}


def main():
    spark = common.get_spark("ingest_bronze")
    cities = read_cities()
    last_day = date.today().replace(day=1) - timedelta(days=1)
    done = already_loaded(spark)
    batch_id = str(uuid.uuid4())
    new_rows = []
    skipped = 0
    try:
        for start, end in month_windows(HISTORY_START, last_day):
            for city in cities:
                key = (city["city"], start.isoformat(), end.isoformat())
                if key in done:
                    skipped += 1
                    continue
                url = build_url(city, start, end)
                status, body = fetch(url)
                new_rows.append((
                    batch_id, datetime.now(timezone.utc), "archive", city["city"],
                    start.isoformat(), end.isoformat(), url, status, body,
                ))
                time.sleep(PAUSE_SECONDS)
    finally:
        if new_rows:
            spark.createDataFrame(new_rows, SCHEMA).write.format("delta").mode("append").save(BRONZE_TABLE)
        failed = sum(1 for row in new_rows if row[7] != 200)
        print("windows skipped (already in bronze):", skipped)
        print("windows loaded now:", len(new_rows))
        print("loaded now with status not 200:", failed)
        if DeltaTable.isDeltaTable(spark, BRONZE_TABLE):
            print("rows in bronze now:", spark.read.format("delta").load(BRONZE_TABLE).count())
    spark.stop()


if __name__ == "__main__":
    main()
