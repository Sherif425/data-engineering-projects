**Project #1 – Weather Data Platform (Upwork ETL Job Simulation)**

This single project will include the following technologies:
`API ingestion → ETL → PostgreSQL → Airflow → Data Quality → Deployment`

---

# 🏗 Project #1 – Cairo Weather Analytics Platform

**Business Story (client brief):**

> “We need an automated pipeline that pulls weather data every hour, stores it in PostgreSQL, tracks changes over time, and provides clean tables for analytics.”

---

## 📦 Tech Stack

| Layer         | Tool               |
| ------------- | ------------------ |
| Extract       | OpenWeatherMap API |
| Transform     | Python + Pandas    |
| Load          | PostgreSQL         |
| Orchestration | Apache Airflow     |
| Versioning    | Git                |
| Infra         | Docker Compose     |

---

## 📁 Folder Structure

```
weather_data_platform/
 ├── docker-compose.yml
 ├── dags/
 │     └── weather_etl_dag.py
 ├── etl/
 │     ├── extract.py
 │     ├── transform.py
 │     └── load.py
 ├── sql/
 │     └── create_tables.sql
 ├── requirements.txt
 └── .env
```

---

## 🔐 1️⃣ Create `.env`

```
POSTGRES_DB=weatherdb
POSTGRES_USER=weather
POSTGRES_PASSWORD=weather123
OPENWEATHER_API_KEY=PUT_YOUR_KEY_HERE
```

---

## 🐘 2️⃣ PostgreSQL Table

`sql/create_tables.sql`

```sql
CREATE TABLE IF NOT EXISTS weather_raw (
    id SERIAL PRIMARY KEY,
    city TEXT,
    temperature FLOAT,
    humidity INT,
    pressure INT,
    wind_speed FLOAT,
    weather_desc TEXT,
    collected_at TIMESTAMP
);
```

---

## 🌐 3️⃣ Extract – `etl/extract.py`

```python
import os, requests
from datetime import datetime

def extract_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Cairo&appid={api_key}&units=metric"
    res = requests.get(url)
    data = res.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "weather_desc": data["weather"][0]["description"],
        "collected_at": datetime.utcnow()
    }
```

---

## 🔄 4️⃣ Transform – `etl/transform.py`

```python
def transform_weather(data):
    data["weather_desc"] = data["weather_desc"].title()
    return data
```

---

## 📥 5️⃣ Load – `etl/load.py`

```python
import psycopg2, os

def load_weather(data):
    conn = psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_raw (city, temperature, humidity, pressure, wind_speed, weather_desc, collected_at)
        VALUES (%(city)s,%(temperature)s,%(humidity)s,%(pressure)s,%(wind_speed)s,%(weather_desc)s,%(collected_at)s)
    """, data)

    conn.commit()
    cur.close()
    conn.close()
```

---

## 🕒 6️⃣ Airflow DAG – `dags/weather_etl_dag.py`

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl.extract import extract_weather
from etl.transform import transform_weather
from etl.load import load_weather

def run_etl():
    data = extract_weather()
    clean = transform_weather(data)
    load_weather(clean)

with DAG("weather_pipeline",
         start_date=datetime(2024,1,1),
         schedule_interval="@hourly",
         catchup=False) as dag:

    etl = PythonOperator(
        task_id="weather_etl",
        python_callable=run_etl
    )
```

---

## 🐳 7️⃣ Docker Compose – `docker-compose.yml`

```yaml
version: '3'
services:
  postgres:
    image: postgres:15
    env_file: .env
    volumes:
      - ./sql:/docker-entrypoint-initdb.d
    ports: ["5432:5432"]

  airflow:
    image: apache/airflow:2.8.1
    env_file: .env
    volumes:
      - ./dags:/opt/airflow/dags
      - ./etl:/opt/airflow/etl
    ports: ["8080:8080"]
    command: standalone
```

---

## 🚀 8️⃣ Run It

```bash
docker compose up -d
```

Open Airflow:
➡ [http://localhost:8080](http://localhost:8080)
Enable **weather_pipeline**

---

## 📊 9️⃣ Verify Data

```sql
SELECT city, temperature, collected_at
FROM weather_raw
ORDER BY collected_at DESC
LIMIT 10;
```


