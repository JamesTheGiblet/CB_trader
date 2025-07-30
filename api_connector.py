import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configs
MAX_RETRIES = 5
BACKOFF_FACTOR = 2
INITIAL_DELAY = 5

def fetch_candles(exchange, symbol, interval):
    url = ""
    headers = {}

    if exchange.lower() == "coinbase":
        url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity={get_granularity(interval)}"
        headers["CB-ACCESS-KEY"] = os.getenv("COINBASE_KEY")

    elif exchange.lower() == "gemini":
        url = f"https://api.gemini.com/v2/candles/{symbol}/{interval}"
        headers["X-GEMINI-APIKEY"] = os.getenv("GEMINI_KEY")

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[API] Error {response.status_code}. Retrying...")
        except requests.exceptions.RequestException as e:
            wait = INITIAL_DELAY * (BACKOFF_FACTOR ** attempt)
            print(f"[API] Exception: {e} | Backing off {wait}s...")
            time.sleep(wait)
    return None

def get_granularity(interval):
    mapping = {"1h": 3600, "4h": 14400, "1d": 86400}
    return mapping.get(interval, 3600)