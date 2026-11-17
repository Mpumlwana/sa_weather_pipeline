# 🧭 Design Decisions and Full Results

This file holds the detail behind the README. It grows with every deliverable. Last updated: Deliverable 1.

---

## 🔬 Deliverable 0: Feasibility test

| Question | Answer |
|---|---|
| Can we reach the Open-Meteo API? | ✅ Yes: the forecast and history endpoints both returned data |
| Does it give history? | ✅ Yes: a daily request for 1 to 3 January 2025 worked |
| Does Spark 4.2.0 with Delta 4.4.1 run on Windows? | ❌ No: Delta needs winutils.exe there |
| Does it run in a Linux container (Docker)? | ✅ Yes: a Delta table was written and read back |
| Does the data survive the container? | ✅ Yes: a mounted folder kept 3 Delta versions (0, 1 and 2) |
| Does a second run duplicate rows? | ✅ No: the table kept 5 rows, and the log shows one add and one remove |

---

## 📥 Deliverable 1: Ingest into bronze

| Question | Answer |
|---|---|
| Which cities? | ✅ 9, one per province, listed in `src/cities.csv` |
| How much history was loaded? | ✅ 198 rows: 22 months (January 2025 to October 2026) for 9 cities |
| Does a second history run add rows? | ✅ No: 198 skipped, 0 added |
| Is the raw JSON stored unchanged? | ✅ Yes: checked 2 degree signs and 0 garbled characters |
| How are recent days loaded? | ✅ The forecast address with past_days=21: 9 rows per run, one per city |
| Does a second recent-days run add rows? | ✅ No: same day, 9 skipped, 0 added |
| How many rows are in bronze now? | ✅ 216: 198 history and 18 forecast (two runs of 9) |
| Do the two sources agree? | ✅ Mostly: for Cape Town, 4 of 5 overlapping days were equal and 1 differed by 0.1 degrees (maximum temperature and rain only) |

**What went wrong, and the fix:**

- A 14-day look-back left 1 and 2 November missing once the run was 3 days later, so it was raised to 21 days
- Hand-counted file sizes were wrong several times, so sizes are now measured by a script

**Not known yet:** whether old values are ever revised, and how many past days the forecast address allows beyond 21.

---

## 📐 Design decisions so far

- Spark and Delta run in a Linux container, with exact versions pinned
- Every API call sends timezone=Africa/Johannesburg, because the default is GMT
- Bronze keeps each API response unchanged, with an ingested_at time and a source (archive or forecast)
- Bronze is append only: a request window already stored with status 200 is skipped, so the pipeline is safe to run twice
- The same day can appear more than once in bronze, so silver will keep one row per city per day
- Today is worked out in South African time (UTC+2), because the container clock is UTC
- Tests run on a saved sample, never on the real API
- Data lives in a mounted folder outside the container, and is never uploaded to GitHub
- Weather only for now: ZAR exchange rates are untested, so they are a later extension
