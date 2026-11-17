# 🌦️ South African Weather Pipeline

> 🚧 **Status: IN PROGRESS.** Built step by step. This file lists only what has been run and checked.

My second data engineering project: a daily pipeline that gets real weather data for 9 South African cities from the Open-Meteo API and keeps it in bronze, silver and gold Delta tables, with data quality checks and automated tests. It never duplicates rows when it runs twice.

📖 More detail: [design decisions and full results](docs/design_decisions.md) · one reflection per deliverable in [`docs/`](docs)

---

## 🗂️ Project Structure

```
sa_weather_pipeline/
├── Dockerfile            # Linux image: Python 3.12, Java, PySpark, Delta
├── .dockerignore         # Files Docker leaves out of the build
├── .gitignore            # Keeps secrets and data out of GitHub
├── README.md             # You are here
├── data/                 # Delta tables (not uploaded to GitHub)
│   ├── bronze/           # weather_raw: raw API responses, never edited
│   ├── silver/           # Planned: cleaned data
│   └── gold/             # Planned: summary tables
├── src/
│   ├── cities.csv        # The 9 cities, one per province
│   ├── common.py         # Shared settings and the Spark session
│   ├── ingest_bronze.py  # History: one month per city, from January 2025
│   └── ingest_recent.py  # Recent days: last 21 days plus today
├── tests/                # Planned: automated tests
└── docs/                 # Reflections and design decisions
```

---

## ✅ Deliverables Overview

| # | Deliverable | Status |
|---|---|---|
| 0 | 🧪 Feasibility test: API, Spark + Delta in Docker, design decisions | ✅ Done |
| 1 | 📥 Ingest into bronze, unchanged (Python): history plus recent days | ✅ Done |
| 2 | 🧹 Clean into silver (PySpark, Delta) | ⬜ Not Started |
| 3 | 🏅 Gold summary tables (PySpark, Delta) | ⬜ Not Started |
| 4 | 🛡️ Data quality checks, tests on every push, architecture diagram | ⬜ Not Started |

---

## 🔬 Results So Far

### 🧪 Deliverable 0: Feasibility test

- ✅ The Open-Meteo forecast and history endpoints both return data
- ❌ Spark 4.2.0 with Delta 4.4.1 fails on Windows (needs winutils.exe), ✅ but works in a Linux Docker container
- ✅ The data survives the container: a mounted folder kept 3 Delta versions
- ✅ A second run did not duplicate rows (the table kept 5 rows)
- 📝 [Reflection](docs/reflection_deliverable_0.md)

### 📥 Deliverable 1: Ingest into bronze

- ✅ 198 history rows (22 months for 9 cities). A second run skipped 198 and added 0
- ✅ Recent days from the forecast address (past_days=21): 9 rows per run. A second run on the same day added 0
- ✅ 216 rows in bronze (198 history and 18 forecast), raw JSON stored unchanged
- ✅ For Cape Town, 4 of 5 overlapping days matched exactly between the two sources and 1 differed by 0.1 degrees
- 📝 [Reflection](docs/reflection_deliverable_1.md) · [Full results and decisions](docs/design_decisions.md)

---

## 🛠️ Tools & Technologies

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![PySpark](https://img.shields.io/badge/PySpark-4.2.0-orange?logo=apachespark)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-4.4.1-00ADD4)
![Docker](https://img.shields.io/badge/Docker-Linux_container-2496ED?logo=docker&logoColor=white)

Planned, not built yet: `pytest` · GitHub Actions

---

## 🚀 How to Run (so far)

1. Install Docker Desktop and wait for Engine running.
2. Build the image (first build downloads about 450 MB):
   ```powershell
   docker build -t sa-weather-pipeline .
   ```
3. Load the history (writes to data\bronze\weather_raw, which Git ignores):
   ```powershell
   docker run --rm -v C:\projects\sa_weather_pipeline:/app -v sa-ivy-cache:/root/.ivy2.5.2 sa-weather-pipeline python src/ingest_bronze.py
   ```
4. Load the recent days (last 21 days plus today):
   ```powershell
   docker run --rm -v C:\projects\sa_weather_pipeline:/app -v sa-ivy-cache:/root/.ivy2.5.2 sa-weather-pipeline python src/ingest_recent.py
   ```

Running either command twice on the same day adds nothing.

---

## 📊 Data Source

**Source:** [Open-Meteo](https://open-meteo.com/). The free API is for non-commercial use, with fewer than 10,000 calls per day, under the CC BY 4.0 licence. Weather data by [Open-Meteo.com](https://open-meteo.com/).

---

## 📬 Connect With Me

**Lakhikhaya Mpumlwana**
[![GitHub](https://img.shields.io/badge/GitHub-Mpumlwana-black?logo=github)](https://github.com/Mpumlwana)

---

⭐ *This repository is actively updated as deliverables are completed.*
