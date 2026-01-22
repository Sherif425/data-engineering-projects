🏗️ Project We’ll Build (Incrementally)
Scenario

“The analytics team needs daily exchange rate data stored in PostgreSQL to support financial reports.”

This is extremely common in banks, fintech, and payments (which fits your background nicely).

🧰 Tech Stack (Locked)

    Python 3.11
    PostgreSQL 16
    Docker + docker-compose
    Pandas
    Requests
    SQLAlchemy
    Logging

.env + YAML config

Git-style project structure

📁 Final Project Structure (You will grow into this)
fx_etl/
│
├── ingest/
│   └── fetch_rates.py
├── transform/
│   └── clean_rates.py
├── load/
│   └── load_postgres.py
│
├── config/
│   └── settings.yaml
│
├── db/
│   └── init.sql
│
├── logs/
│
├── main.py
├── docker-compose.yml
├── requirements.txt
└── .env


This structure is CV-worthy.

🚀 STEP 1 — Environment Setup (Today’s Task)
Option A: Docker (Preferred, Professional)

Create this docker-compose.yml:

    version: "3.9"

    services:
    postgres:
        image: postgres:16
        container_name: fx_postgres
        environment:
        POSTGRES_DB: fx_dw
        POSTGRES_USER: etl_user
        POSTGRES_PASSWORD: etl_pass
        ports:
        - "5432:5432"
        volumes:
        - pgdata:/var/lib/postgresql/data

    volumes:
    pgdata:


Run:

    docker compose up -d


Verify:

    psql -h localhost -U etl_user -d fx_dw

📄 Create Database Table (Very Important)

Create db/init.sql:

    CREATE TABLE IF NOT EXISTS exchange_rates (
        rate_date DATE NOT NULL,
        base_currency VARCHAR(3) NOT NULL,
        target_currency VARCHAR(3) NOT NULL,
        rate NUMERIC(12,6) NOT NULL,
        source VARCHAR(50),
        created_at TIMESTAMP DEFAULT NOW(),
        PRIMARY KEY (rate_date, base_currency, target_currency)
    );


👉 Notice:

Composite primary key

Idempotent loads (no duplicates)

Analytics-friendly

🌐 STEP 2 — Data Source (We Lock This)

We’ll use:

https://api.exchangerate.host/latest


Example response:

{
  "base": "EUR",
  "date": "2024-01-20",
  "rates": {
    "USD": 1.08,
    "EGP": 33.5
  }
}

🧠 STEP 3 — Your First Task (DO THIS)
🎯 Task A

Create:

ingest/fetch_rates.py


It must:

Call the API

Parse JSON

Return structured Python data

Handle errors

Skeleton (you fill logic):

    import requests
    from datetime import date

    API_URL = "https://api.exchangerate.host/latest"

    def fetch_rates(base="EUR"):
        response = requests.get(API_URL, params={"base": base}, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "date": data["date"],
            "base": data["base"],
            "rates": data["rates"]
        }

    if __name__ == "__main__":
        print(fetch_rates())

🧪 Definition of Done (Very Important)

You are done when:

PostgreSQL is running

Table exists

fetch_rates.py prints clean data

No Pandas yet

No loading yet

🧠 Mindset Check

You are not learning random topics anymore.
You are executing a pipeline lifecycle:

Ingest → Transform → Load → Validate → Automate

✅ Reply With:

✔️ Docker running or not

✔️ Output of fetch_rates.py

❓ Any error (copy-paste)

Next step after that:
👉 Transform → Pandas → normalization → PostgreSQL load

You’re officially on track now. 🚀