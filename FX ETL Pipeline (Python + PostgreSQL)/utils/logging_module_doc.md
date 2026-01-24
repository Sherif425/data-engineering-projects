# 🧠 First: What Logging REALLY Is (Mental Model)

### ❌ What beginners do

```python
print("Starting ETL")
print("Data fetched")
print("Something failed")
```

Problems:

* Lost when script exits
* No timestamps
* No severity
* No history
* Impossible to debug in production

---

### ✅ What professionals do

They answer **these questions without rerunning code**:

* When did the pipeline start?
* Which step failed?
* How many rows were processed?
* Was it a warning or a fatal error?
* What happened yesterday at 3 AM?

That’s **logging**.

---

# 📦 Python Logging Module (Core Concepts)

Python’s built-in `logging` module gives you:

## 1️⃣ Log Levels (VERY IMPORTANT)

| Level    | When to Use                          |
| -------- | ------------------------------------ |
| DEBUG    | Internal details (dev only)          |
| INFO     | Normal pipeline progress             |
| WARNING  | Something odd but pipeline continues |
| ERROR    | Step failed, pipeline affected       |
| CRITICAL | Pipeline must stop immediately       |

👉 **Rule of thumb**:

* INFO = business visibility
* ERROR = wake someone up

---

## 2️⃣ Log Message Anatomy

A professional log line looks like this:

```
2026-01-21 10:02:15 | INFO | ingest.fetch_rates | Fetched 29 FX rates
```

It tells you:

* When
* Severity
* Where
* What happened

---

# 🏗️ Step 1 — Central Logging Configuration

Create:

```
config/logging_config.py
```

```python
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "etl.log")

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler (rotating!)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5_000_000, backupCount=5
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
```

📌 **Why rotating logs?**

* Prevent disk from filling up
* Keep history (etl.log.1, etl.log.2, …)

---

# 🔗 Step 2 — Use Logging in Each ETL Step

## Ingest (`fetch_rates.py`)

```python
import logging
import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.frankfurter.app/latest"

def fetch_rates(base="EUR"):
    logger.info("Fetching FX rates with base=%s", base)

    response = requests.get(API_URL, params={"from": base}, timeout=10)
    response.raise_for_status()

    data = response.json()
    rate_count = len(data.get("rates", {}))

    logger.info("Fetched %d FX rates", rate_count)

    return {
        "date": data["date"],
        "base": data["base"],
        "rates": data["rates"]
    }
```

📌 Notice:

* No `print`
* Context-rich messages
* `%s` formatting (lazy & efficient)

---

## Transform (`clean_rates.py`)

```python
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def normalize_rates(raw_data):
    logger.info("Normalizing FX data for date %s", raw_data["date"])

    records = [
        {
            "rate_date": raw_data["date"],
            "base_currency": raw_data["base"],
            "target_currency": k,
            "rate": v
        }
        for k, v in raw_data["rates"].items()
    ]

    df = pd.DataFrame(records)

    logger.info("Normalized into %d rows", len(df))

    return df
```

---

## Load (`load_postgres.py`)

```python
import logging

logger = logging.getLogger(__name__)

def load_rates(df):
    logger.info("Loading %d rows into PostgreSQL", len(df))

    # (DB code here)

    logger.info("Load completed successfully")
```

---

# 🚀 Step 3 — Initialize Logging Once (main.py)

```python
from config.logging_config import setup_logging
from ingest.fetch_rates import fetch_rates
from transform.clean_rates import normalize_rates
from load.load_postgres import load_rates
import logging

logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("ETL pipeline started")

    raw_data = fetch_rates()
    df = normalize_rates(raw_data)
    load_rates(df)

    logger.info("ETL pipeline finished successfully")

if __name__ == "__main__":
    setup_logging()
    run_pipeline()
```

---

# 📄 What Your `etl.log` Will Look Like

```
2026-01-21 10:00:01 | INFO | __main__ | ETL pipeline started
2026-01-21 10:00:02 | INFO | ingest.fetch_rates | Fetching FX rates with base=EUR
2026-01-21 10:00:03 | INFO | ingest.fetch_rates | Fetched 29 FX rates
2026-01-21 10:00:03 | INFO | transform.clean_rates | Normalizing FX data for date 2026-01-21
2026-01-21 10:00:03 | INFO | transform.clean_rates | Normalized into 29 rows
2026-01-21 10:00:04 | INFO | load.load_postgres | Loading 29 rows into PostgreSQL
2026-01-21 10:00:05 | INFO | load.load_postgres | Load completed successfully
2026-01-21 10:00:05 | INFO | __main__ | ETL pipeline finished successfully
```

This is **production-grade visibility**.

---

# 🧠 Why Logging Is a Career Skill (Not Just Code)

When you interview and say:

> “I add structured logging with severity levels and rotating files”

That’s **mid-level engineer language**, not junior.

---

# 🔜 NEXT (When You’re Ready)

Next logical upgrades:

1. Log **rows in vs rows loaded**
2. Log **execution time**
3. Log **exceptions with stack traces**
4. Fail pipeline gracefully

If you want, next message I can:

* Add **try/except + logging.exception**
* Or refactor logging to **JSON logs**
* Or integrate logging with **Airflow later**

Tell me which one you want 👇
