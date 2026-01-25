import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from psycopg2.extras import execute_batch
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

UPSERT_SQL = """
INSERT INTO exchange_rates (
    rate_date,
    base_currency,
    target_currency,
    rate,
    source
)
VALUES (
    %(rate_date)s,
    %(base_currency)s,
    %(target_currency)s,
    %(rate)s,
    'frankfurter'
)
ON CONFLICT (rate_date, base_currency, target_currency)
DO UPDATE SET
    rate = EXCLUDED.rate,
    created_at = NOW();
"""
def load_exchange_rates(df):
    logger.info(f"Loading {len(df)} rows into PostgreSQL (batch)")

    engine = create_engine(DB_URL)
    records = df.to_dict(orient="records")

    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()
        execute_batch(cursor, UPSERT_SQL, records, page_size=500)
        conn.commit()

        logger.info(
            f"Batch load completed | rows_loaded={len(records)}"
        )

    finally:
        cursor.close()
        conn.close()
