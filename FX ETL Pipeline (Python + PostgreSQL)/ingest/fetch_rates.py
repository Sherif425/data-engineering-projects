import requests
from datetime import date
from utils.logger import get_logger

logger = get_logger(__name__)

API_URL= "https://api.frankfurter.app/latest"

def fetch_rates(base="EUR"):
    response = requests.get(API_URL, params={"from": base}, timeout=10)
    response.raise_for_status()
   
    data = response.json()
   

    # logger.info(
    #     "Fetched FX rates",
    #     extra={"base": data["base"], "count": len(data["rates"])}
    # )

    logger.info(
        f"Fetched FX rates | base={data['base']} | count={len(data['rates'])}"
    )

    return {
        "date": data["date"],
        "base": data["base"],
        "rates": data["rates"]
    }

if __name__ == "__main__":
    print(fetch_rates())
