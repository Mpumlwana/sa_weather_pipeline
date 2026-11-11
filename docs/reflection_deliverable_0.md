# 📝 Reflection - Deliverable 0: Feasibility Test

## 🎯 What I Did

Before building anything, I tested whether Project 2 is possible on my own computer. I called the Open-Meteo API, ran Spark and Delta, and made the first design decisions. Then I put the project on GitHub.

- Called the Open-Meteo forecast API for Cape Town and got real data: 27.1 °C at 15:15 UTC on 4 November 2026
- Called the history API for 1 to 3 January 2025 and got daily maximums of 23.5, 25.3 and 27.3 °C
- Read the official terms: free for non-commercial use, under 10,000 calls a day, CC BY 4.0
- Installed PySpark 4.2.0 and delta-spark 4.4.1 and started Spark on Windows
- Moved the work into a Linux Docker container, wrote a Dockerfile, and wrote and read a Delta table there
- Showed that the data survives the container (bind mount) and that a second run does not duplicate rows
- Pushed the first commit to GitHub

## 💡 What I Learned

- ✅ Test the risky things first: the API worked, but Delta did not run on Windows
- ✅ Odd data is not wrong data: the API moved my point (-33.9249, 18.4241) to its own grid point (-33.989456, 18.426968)
- ✅ Times come back in GMT unless I send timezone=Africa/Johannesburg, so every call must send it
- ✅ Read the first real error, not the last line: JAVA_GATEWAY_EXITED was only a result, the cause was a missing slf4j-api jar
- ✅ No error does not mean it works: pip installed Spark without a problem, but Delta only failed when it wrote files
- ✅ Delta is plain files: a Parquet file plus a _delta_log folder, and an overwrite adds a new file and removes the old one in the log, so the table kept 5 rows
- ✅ Look before you fix: I renamed folders and did not delete them, so every change could be undone
- ✅ Predictions can be wrong: I compared every result with what I expected, and wrote down the misses

## 🧗 Challenges I Faced

- 🐢 The PySpark download was 450.1 MB and took 46 minutes on my Wi-Fi
- 🧩 Spark failed three times on slf4j-api 2.0.13: an old Maven folder had the description file but not the jar, and Ivy had saved a note that pointed to it. Renaming the Maven folder was not enough, I also had to rename the org.slf4j folder in the Ivy cache
- 🪟 Delta failed on Windows because HADOOP_HOME and winutils.exe were missing. I chose Docker (Linux) and not an unverified .exe
- 🔐 In the container, spark-submit had no execute permission, because the PySpark wheel was built on Windows. A chmod fixed it for the test image
- 🔁 The real Dockerfile installs PySpark from PyPI and did not need the chmod fix
- ⏱️ Setup took from 30 October to 11 November, longer than I wanted, and I asked to change the way we worked

## 🛠️ Tools Used

`Python 3.12` · `PySpark 4.2.0` · `Delta Lake 4.4.1` · `Docker` · `Open-Meteo API` · `PowerShell` · `Git` · `GitHub`

---

*Deliverable 0 of the sa_weather_pipeline project*
