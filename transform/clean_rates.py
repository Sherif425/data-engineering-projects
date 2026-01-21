import pandas as pd
def normalize_rates(raw_data: dict) -> pd.DataFrame:
    """
    Convert raw FX API response into normalized tabular format
    """

    records = []

    for target_currency, rate in raw_data["rates"].items():
        records.append({
            "rate_date": raw_data["date"],
            "base_currency": raw_data["base"],
            "target_currency": target_currency,
            "rate": rate
        })

    df = pd.DataFrame(records)
    print("df\n", df)
    
    # ---- Basic data quality checks ----
    assert not df.empty, "DataFrame is empty"
    assert df["rate"].notnull().all(), "Null rates detected"
    assert df["rate"].gt(0).all(), "Invalid (<=0) rates found"

    return df


if __name__ == "__main__":
    # manual test
    sample = {
        "date": "2026-01-20",
        "base": "EUR",
        "rates": {
            "USD": 1.17,
            "EGP": 33.4
        }
    }
    print("\n",normalize_rates(sample))
