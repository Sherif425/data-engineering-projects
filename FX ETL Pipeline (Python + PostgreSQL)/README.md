# FX ETL Pipeline (Python + PostgreSQL)

A **production-style ETL pipeline** built with Python that ingests daily foreign exchange (FX) rates from a public API, transforms and validates the data, and loads it into PostgreSQL using **idempotent UPSERT logic**.

This project is intentionally designed to reflect **real-world data engineering practices**, not one-off scripts.

---

## 📌 Project Overview

**Scenario**
Analytics teams often require reliable, daily FX rates to support reporting and financial analysis. This pipeline automates the full lifecycle:

1. **Ingest** FX rates from an external API
2. **Transform** semi-structured JSON into normalized tabular data
3. **Validate** data quality assumptions
4. **Load** data safely into PostgreSQL
5. Support **re-runs without duplication** (idempotency)

---

## 🧱 Architecture

```
API (Frankfurter)
   ↓
Ingestion (Python requests)
   ↓
Transformation (Pandas)
   ↓
Validation (assertions)
   ↓
PostgreSQL (UPSERT)
```

---

## 🛠️ Tech Stack

* **Python 3.11**
* **PostgreSQL 16**
* **Docker & Docker Compose**
* **Pandas**
* **SQLAlchemy + psycopg2**
* **python-dotenv**

---

## 📁 Project Structure

```
fx_etl/
│
├── ingest/
│   └── fetch_rates.py        # API ingestion
├── transform/
│   └── clean_rates.py        # Normalization & data quality checks
├── load/
│   └── load_postgres.py      # PostgreSQL UPSERT loader
│
├── db/
│   └── init.sql              # Database schema
├── config/
│   └── settings.yaml         # (reserved for future use)
│
├── logs/                     # (reserved for logging)
├── main.py                   # Pipeline entry point
├── docker-compose.yml        # PostgreSQL service
├── requirements.txt
├── .env                      # Environment variables (not committed)
└── README.md
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE exchange_rates (
    rate_date DATE NOT NULL,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate NUMERIC(12,6) NOT NULL,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (rate_date, base_currency, target_currency)
);
```

* Composite primary key enables **UPSERT logic**
* Prevents duplicates on re-runs

---

## ⚙️ Setup & Run

### 1️⃣ Start PostgreSQL (Docker)

```bash
docker compose up -d
```

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fx_dw
DB_USER=etl_user
DB_PASSWORD=etl_pass
```

---

### 4️⃣ Run the Pipeline

```bash
python main.py
```

You can safely run the pipeline **multiple times** — data will be updated, not duplicated.

---

## ✅ Data Quality Checks

Implemented during transformation:

* Dataset must not be empty
* No null exchange rates
* All rates must be positive

Failures stop the pipeline early to avoid corrupting downstream data.

---

## 🔁 Idempotency

The loader uses PostgreSQL `ON CONFLICT DO UPDATE`:

* Same `(date, base, target)` → **UPDATE**
* New combination → **INSERT**

This makes the pipeline **safe to retry** and suitable for scheduling.

---

## 🚀 Why This Project Matters

Unlike many tutorial-style ETL examples, this project demonstrates:

* Clear separation of ingest / transform / load layers
* Explicit SQL instead of black-box helpers
* Transaction safety
* Environment-based configuration
* Production-ready data modeling

---

## 🔮 Possible Extensions

* Add structured logging
* Schedule with cron or Apache Airflow
* Add incremental loading logic
* Extend to ELT (warehouse-side transformations)
* Add unit tests for transformations

---

## 👤 Author

Built as part of a hands-on data engineering learning track.

---

## 📄 License

MIT License
