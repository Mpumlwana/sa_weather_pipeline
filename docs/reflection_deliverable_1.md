# 📝 Reflection - Deliverable 1: Ingest into Bronze (Python)

## 🎯 What I Did

- Set up a Docker volume called `sa-ivy-cache` that keeps the Delta jar files, so a run dropped from 96 seconds to 52 seconds
- Used the Open-Meteo geocoding address to pick 9 cities, one per province, and saved them in `src/cities.csv` (9 rows)
- Wrote `common.py` (shared settings and the Spark session) and `ingest_bronze.py`, which asks the history address for one month per city, from January 2025 to the last full month
- Stored every response unchanged in the Delta table `weather_raw`, with batch id, ingested_at, source, address and status code
- First run loaded 198 rows (22 per city). The second run skipped 198 and added 0
- Checked that the raw JSON was stored unchanged: 2 degree signs and 0 garbled characters
- Tested the forecast address with past_days=14, then wrote `ingest_recent.py` for the days after the last full month
- Found a gap, raised the look-back to 21 days (22 dates returned), and loaded 9 more rows. The second run of the same window skipped 9
- Compared 5 overlapping days for Cape Town between the history and forecast sources
- Committed and pushed the code to GitHub

## 💡 What I Learned

- ✅ Bronze keeps the raw response text and the status code, so the data can always be processed again later
- ✅ Skipping a window that is already in bronze with status 200 makes the ingest safe to run twice
- ✅ A Docker volume can cache downloaded jars, so the next runs start faster
- ✅ The container clock is UTC, so the script uses South African time (UTC+2) to decide what today is
- ✅ The same day can come from two sources: 4 of 5 days matched exactly and 29 October differed by 0.1 degrees
- ✅ Because of that, bronze will hold some days twice, and silver needs a rule to keep one row per city per day

## 🧗 Challenges I Faced

- A 14-day look-back only covered the gap on the day I tested it. Three days later the window started on 3 November and 1 and 2 November were missing, which I saw in the printed window
- My hand-counted file sizes were wrong several times, so I switched to sizes measured by a script. In this deliverable the checks (1193 bytes, 2518 bytes, 77 lines) all matched
- Pasted output arrived in a confusing order once, so I ran one extra check instead of guessing the file state
- I still do not know if old values are ever revised, or how many past days the forecast address allows beyond 21

## 🛠️ Tools Used

`Python` · `PySpark` · `Delta Lake` · `Docker` · `PowerShell` · `Git` · `GitHub` · `Open-Meteo API`

---

*Deliverable 1 of the South African Weather Pipeline project*
