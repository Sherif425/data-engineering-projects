from ingest.fetch_rates import fetch_rates
from transform.clean_rates import normalize_rates
from load.load_postgres import load_exchange_rates
from utils.logger import get_logger

logger = get_logger("pipeline")

def run_pipeline():

    logger.info("ETL pipeline started")
    
    raw_data = fetch_rates(base="EUR")
    df = normalize_rates(raw_data)
    load_exchange_rates(df)

    # print("\n\nDataFrame Head:\n\n", df.head())
    # print("\n\n Row Count: \n\n", df.count())

    logger.info("ETL pipeline finished successfully", extra={"row": len(df)})

if __name__ == "__main__":
    run_pipeline()
