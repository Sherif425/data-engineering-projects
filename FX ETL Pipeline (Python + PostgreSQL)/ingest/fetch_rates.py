import requests
from datetime import date

API_URL= "https://api.frankfurter.app/latest"

def fetch_rates(base="EUR"):
    response = requests.get(API_URL, params={"from": base}, timeout=10)
    response.raise_for_status()
    data = response.json()
    # print(data)

    return {
        "date": data["date"],
        "base": data["base"],
        "rates": data["rates"]
    }

if __name__ == "__main__":
    print(fetch_rates())
