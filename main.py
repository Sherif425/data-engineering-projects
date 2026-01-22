from ingest.fetch_rates import fetch_rates
from transform.clean_rates import normalize_rates
from load.load_postgres import load_exchange_rates

def run_pipeline():
    raw_data = fetch_rates(base="EUR")
    df = normalize_rates(raw_data)
    load_exchange_rates(df)

    print("\n\nDataFrame Head:\n\n", df.head())
    print("\n\n Row Count: \n\n", df.count())


if __name__ == "__main__":
    run_pipeline()
