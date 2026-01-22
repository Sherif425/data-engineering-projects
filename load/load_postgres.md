
---

# 📄 `load/load_postgres.py` — FULL DEEP DIVE

Here is the full file again for reference:

```python
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL, future=True)


def load_exchange_rates(df):
    """
    Load FX rates into PostgreSQL using UPSERT logic.
    """

    upsert_sql = text("""
        INSERT INTO exchange_rates (
            rate_date,
            base_currency,
            target_currency,
            rate,
            source
        )
        VALUES (
            :rate_date,
            :base_currency,
            :target_currency,
            :rate,
            :source
        )
        ON CONFLICT (rate_date, base_currency, target_currency)
        DO UPDATE SET
            rate = EXCLUDED.rate,
            source = EXCLUDED.source;
    """)

    records = df.to_dict(orient="records")

    for r in records:
        r["source"] = "frankfurter"

    with engine.begin() as conn:
        conn.execute(upsert_sql, records)
```

Now let’s **peel it layer by layer**.

---

## 1️⃣ Imports (Nothing Fancy Yet)

```python
import os
```

* Gives access to environment variables
* Used to read DB credentials safely

📌 Why this matters:
Hardcoding passwords is **unacceptable** in production.

---

```python
from sqlalchemy import create_engine, text
```

Two things here:

### 🔹 `create_engine`

* Creates a **database connection factory**
* Does NOT open a connection yet

Think of it as:

> “Here’s how to connect when needed.”

---

### 🔹 `text`

* Tells SQLAlchemy:

> “This is **raw SQL**, don’t try to ORM it.”

We use it because:

* ETL prefers **explicit SQL**
* `ON CONFLICT` is not ORM-friendly

---

```python
from dotenv import load_dotenv
```

* Loads `.env` file into environment variables
* Makes `os.getenv()` work locally

Without this:

```python
os.getenv("DB_USER")  # would be None
```

---

## 2️⃣ Load Environment Variables

```python
load_dotenv()
```

This line:

* Reads `.env`
* Injects values into the process environment

📌 After this:

```python
os.getenv("DB_USER")  # "etl_user"
```

No magic. Just loading text into memory.

---

## 3️⃣ Build the Database URL (VERY IMPORTANT)

```python
DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)
```

This builds:

```
postgresql+psycopg2://etl_user:etl_pass@localhost:5432/fx_dw
```

### Why this format?

SQLAlchemy requires:

```
dialect+driver://user:password@host:port/database
```

* `postgresql` → DB type
* `psycopg2` → Python driver

---

### ❗ Why Not `psycopg2.connect()`?

Because:

* SQLAlchemy handles pooling
* Transactions are easier
* Works the same across DBs

This is **industry standard**.

---

## 4️⃣ Create the Engine

```python
engine = create_engine(DB_URL, future=True)
```

This does NOT connect yet.

It just says:

> “When I need DB access, use this configuration.”

`future=True`:

* Uses SQLAlchemy 2.0 style behavior
* Safer and more explicit

---

## 5️⃣ Define the Loader Function

```python
def load_exchange_rates(df):
```

Input:

* `df` → Pandas DataFrame (from transform step)

No return value:

* Loader’s job is **side effect** (writing to DB)

---

## 6️⃣ Define the UPSERT SQL

```python
upsert_sql = text("""
    INSERT INTO exchange_rates (
        rate_date,
        base_currency,
        target_currency,
        rate,
        source
    )
    VALUES (
        :rate_date,
        :base_currency,
        :target_currency,
        :rate,
        :source
    )
```

### 🔹 `:rate_date` etc.

These are **named parameters**.

SQLAlchemy will replace them safely from Python dicts.

🚫 No string concatenation
🚫 No SQL injection
✅ Safe & fast

---

### 🔹 `ON CONFLICT`

```sql
ON CONFLICT (rate_date, base_currency, target_currency)
DO UPDATE SET
    rate = EXCLUDED.rate,
    source = EXCLUDED.source;
```

Meaning:

* If row exists → UPDATE
* If not → INSERT

📌 This relies on the **PRIMARY KEY**.

---

## 7️⃣ Convert DataFrame → Records

```python
records = df.to_dict(orient="records")
```

Example output:

```python
[
  {
    "rate_date": "2026-01-20",
    "base_currency": "EUR",
    "target_currency": "USD",
    "rate": 1.17
  },
  ...
]
```

Exactly matches our SQL placeholders.

---

## 8️⃣ Add Metadata (`source`)

```python
for r in records:
    r["source"] = "frankfurter"
```

Why not in transform?

* This is **lineage metadata**
* Belongs to the **load layer**

This is an important design decision.

---

## 9️⃣ Execute Inside a Transaction (CRITICAL)

```python
with engine.begin() as conn:
    conn.execute(upsert_sql, records)
```

This does a LOT:

### 🔹 `engine.begin()`

* Opens a transaction
* Commits automatically if success
* Rolls back if error

### 🔹 `conn.execute(upsert_sql, records)`

* Executes **bulk insert**
* One DB round-trip
* Fast & safe

---

## 🧠 What Happens If Something Fails?

* Network issue?
* Constraint violation?
* Syntax error?

👉 **Nothing is committed.**
Your database stays clean.

---

## 🧩 Mental Model (Burn This In)

```text
DataFrame
   ↓
list[dict]
   ↓
parameterized SQL
   ↓
transaction
   ↓
UPSERT into DB
```

No black boxes.

---

## 🧪 Your Homework (VERY IMPORTANT)

Before we move on, do this **without copying**:

1. Rewrite `DB_URL` construction from memory
2. Explain (in your own words):

   * Why `engine.begin()` is used
   * Why we don’t use `df.to_sql()`
3. Change `"frankfurter"` to a variable

When you reply, **explain**, don’t paste code.

Once you can explain this file, **you officially own this skill**.
