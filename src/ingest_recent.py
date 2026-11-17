"""Load the last 21 days (plus today) from the forecast API into bronze."""

import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from pyspark.sql import functions as F

import common
import ingest_bronze as ib

SOURCE = "forecast"
PAST_DAYS = 21
SA_TIME = timezone(timedelta(hours=2))


def build_url(city):
    """The forecast address: last PAST_DAYS days plus today."""
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "daily": ",".join(common.DAILY_VARIABLES),
        "timezone": common.TIMEZONE,
        "past_days": PAST_DAYS,
        "forecast_days": 1,
    }
    return common.FORECAST_URL + "?" + urlencode(params)


def already_loaded(spark):
    """Windows already in bronze for this source with status 200."""
    try:
        df = spark.read.format("delta").load(ib.BRONZE_TABLE)
    except Exception:
        return set()
    keep = (F.col("http_status") == 200) & (F.col("source") == SOURCE)
    rows = df.filter(keep).select("city", "start_date", "end_date").collect()
    return {(r["city"], r["start_date"], r["end_date"]) for r in rows}


def main():
    spark = common.get_spark("ingest_recent")
    today = datetime.now(SA_TIME).date()
    start = str(today - timedelta(days=PAST_DAYS))
    end = str(today)
    done = already_loaded(spark)
    batch_id = str(uuid.uuid4())
    new_rows = []
    skipped = 0
    bad = 0
    try:
        for city in ib.read_cities():
            if (city["city"], start, end) in done:
                skipped += 1
                continue
            url = build_url(city)
            status, body = ib.fetch(url)
            if status != 200:
                bad += 1
            now = datetime.now(timezone.utc)
            new_rows.append((batch_id, now, SOURCE, city["city"], start, end, url, status, body))
            ib.time.sleep(ib.PAUSE_SECONDS)
    finally:
        if new_rows:
            df = spark.createDataFrame(new_rows, ib.SCHEMA)
            df.write.format("delta").mode("append").save(ib.BRONZE_TABLE)
        total = spark.read.format("delta").load(ib.BRONZE_TABLE).count()
        print("window:", start, "to", end)
        print("skipped (already in bronze):", skipped)
        print("loaded now:", len(new_rows) - bad)
        print("status not 200:", bad)
        print("rows in bronze now:", total)
        spark.stop()


if __name__ == "__main__":
    main()
