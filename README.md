# 🌦️ South African Weather Pipeline

> 🚧 **Status: IN PROGRESS.** Built step by step. This file lists only what has been run and checked.

Welcome! This repository is my second data engineering project: a daily pipeline that gets real weather data for South African cities from the Open-Meteo API, keeps it in bronze, silver and gold Delta tables, and proves it works with data quality checks and automated tests.

---

## 👋 About This Project

Weather data is public, but it arrives as raw API responses. This project turns those responses into clean, trusted tables that grow every day, and that never duplicate rows when the pipeline runs twice.

For every deliverable, you will find:

- 🐍 The code used to build it
- 📊 The results, with real counts
- 💭 A reflection covering what I learned and challenges I faced

---

## 🗂️ Project Structure

```
sa_weather_pipeline/
│
├── Dockerfile            # Linux image: Python 3.12, Java, PySpark, Delta
├── .dockerignore         # Files Docker leaves out of the build
├── .gitignore            # Keeps secrets and data out of GitHub
├── test_delta.py         # Step 0 test: write and read a Delta table
├── README.md             # You are here
│
├── data/                 # Delta tables (not uploaded to GitHub)
│   ├── bronze/           # Planned: raw API responses, never edited
│   ├── silver/           # Planned: cleaned data
│   └── gold/             # Planned: summary tables
│
├── src/                  # Planned: pipeline code
├── tests/                # Planned: automated tests
└── docs/                 # Planned: one reflection per deliverable
```

---

## ✅ Deliverables Overview

| # | Deliverable | Status |
|---|---|---|
| 0 | 🧪 Feasibility test: API, Spark + Delta in Docker, design decisions | ✅ Done |
| 1 | 📥 Ingest into bronze, unchanged (Python) | ⬜ Not Started |
| 2 | 🧹 Clean into silver (PySpark, Delta) | ⬜ Not Started |
| 3 | 🏅 Gold summary tables (PySpark, Delta) | ⬜ Not Started |
| 4 | 🛡️ Data quality checks, tests on every push, architecture diagram | ⬜ Not Started |

---

## 🔬 Results of Deliverable 0

| Question | Answer |
|---|---|
| Can we reach the Open-Meteo API? | ✅ Yes: the forecast and history endpoints both returned data |
| Does it give history? | ✅ Yes: a daily request for 1 to 3 January 2025 worked |
| Does Spark 4.2.0 with Delta 4.4.1 run on Windows? | ❌ No: Delta needs winutils.exe there |
| Does it run in a Linux container (Docker)? | ✅ Yes: a Delta table was written and read back |
| Does the data survive the container? | ✅ Yes: a mounted folder kept 3 Delta versions (0, 1 and 2) |
| Does a second run duplicate rows? | ✅ No: the table kept 5 rows, and the log shows one add and one remove |

**Design decisions so far:**

- Spark and Delta run in a Linux container, with exact versions pinned
- Every API call sends timezone=Africa/Johannesburg, because the default is GMT
- Bronze keeps each API response unchanged, with an ingested_at time
- Tests run on a saved sample, never on the real API
- Data lives in a mounted folder outside the container, and is never uploaded to GitHub
- Weather only for now: ZAR exchange rates are untested, so they are a later extension

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
3. Run the Delta test (writes a table into data\mount_test, which Git ignores):
   ```powershell
   docker run --rm -v C:\projects\sa_weather_pipeline:/app -v C:\projects\sa_weather_pipeline\data\mount_test:/app/delta_test sa-weather-pipeline python test_delta.py
   ```

---

## 📊 Data Source

**Source:** [Open-Meteo](https://open-meteo.com/)

The free API is for non-commercial use, with fewer than 10,000 calls per day, under the CC BY 4.0 licence. Weather data by [Open-Meteo.com](https://open-meteo.com/).

---

## 📬 Connect With Me

**Lakhikhaya Mpumlwana**
[![GitHub](https://img.shields.io/badge/GitHub-Mpumlwana-black?logo=github)](https://github.com/Mpumlwana)

---

⭐ *This repository is actively updated as deliverables are completed.*