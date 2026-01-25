import time
from ingest.fetch_rates import fetch_rates
from transform.clean_rates import normalize_rates
from load.load_exchange_rates import load_exchange_rates
from utils.logger import get_logger

logger = get_logger("pipeline")

def run_pipeline():

    start_time = time.time()
    status = "SUCCESS"

    try:
        logger.info("ETL pipeline started")
        
        raw_data = fetch_rates(base="EUR")
        rows_fetched = len(raw_data['rates'])

        df = normalize_rates(raw_data)
        rows_loaded = len(df)

        load_exchange_rates(df)

        duration = round(time.time() - start_time, 2)
        print(rows_fetched, " ", rows_loaded, " ", duration)
        logger.info(
            f"FX ETL pipeline finished |"
            f"rows_fetched={rows_fetched} | "
            f"rows_loaded={rows_loaded} | "
            f"duration_seconds={duration} |"
            f"status={status}"           
            )
        
    except Exception as exc:
        duration = round(time.time() - start_time, 2)
        status = "FAILED"

        logger.exception(
            "FX ETL pipeline failed",
            extra={
                "duration_seconds": duration,
                "status": status
            }

        )
        raise
    # print("\n\nDataFrame Head:\n\n", df.head())
    # print("\n\n Row Count: \n\n", df.count())

    #logger.info("ETL pipeline finished successfully", extra={"row": len(df)})

if __name__ == "__main__":
    run_pipeline()
