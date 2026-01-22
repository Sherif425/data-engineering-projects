import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from utils.logger import get_logger


logger = get_logger(__name__)

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
    
    logger.info("Loading FX rates into PostgreSQL", extra={"rows": len(df)})


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

    
    logger.info("Load completed successfully")    