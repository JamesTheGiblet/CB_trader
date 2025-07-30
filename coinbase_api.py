"""
The Scribe — handles communication with the Coinbase spirits (API).
"""
import os
import time
import jwt
import requests
import logging
import pandas as pd
from uuid import uuid4


def fetch_candlestick_data(pair: str) -> pd.DataFrame | None:
    """
    Fetches candlestick data for a given pair from the Coinbase v3 API.
    """
    try:
        api_key = os.getenv("COINBASE_API_KEY")
        api_secret = os.getenv("COINBASE_API_SECRET")

        # Un-escape newline characters for the private key from the .env file.
        if api_secret:
            # The key is read as a single line with literal '\\n' sequences.
            api_secret = api_secret.replace('\\n', '\n')

        if not api_key or not api_secret:
            logging.error(
                "Authentication failed. COINBASE_API_KEY and/or "
                "COINBASE_API_SECRET not set in .env file."
            )
            return None

        base_url = "https://api.coinbase.com"
        path = f"/api/v3/brokerage/products/{pair}/candles"
        params = {"granularity": "FIVE_MINUTE"}

        # Generate JWT token for authentication.
        # The 'uri' must match the method and path (without query parameters).
        token = jwt.encode(
            {
                "sub": api_key,
                "iss": "coinbase-cloud",
                "nbf": int(time.time()),
                "exp": int(time.time()) + 60,  # Token is valid for 60 seconds
                "aud": ["retail_rest_api_proxy"],
                "uri": f"GET {base_url.replace('https://', '')}{path}",
            },
            api_secret,
            algorithm="ES256",
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.get(f"{base_url}{path}", headers=headers, params=params)
        # This will raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        data = response.json()
        candles = data.get("candles", [])

        if not candles:
            logging.warning(f"No candlestick data returned for {pair}.")
            return pd.DataFrame() # Return empty DataFrame

        # Convert to DataFrame. Columns are: start, low, high, open, close, volume
        df = pd.DataFrame(
            candles, columns=["start", "low", "high", "open", "close", "volume"]
        )
        df["start"] = pd.to_datetime(df["start"], unit="s")
        for col in ["low", "high", "open", "close", "volume"]:
            df[col] = pd.to_numeric(df[col])

        return df.set_index("start").sort_index()

    except requests.exceptions.HTTPError as e:
        logging.error(f"A curse upon the connection: Could not fetch data for {pair}. Error: {e}")
        if e.response.status_code == 401:
            logging.error("Authentication failed (401). Check your .env file and ensure your system clock is synchronized.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching data for {pair}: {e}")
        if hasattr(e, "response") and getattr(e.response, "status_code", None) == 401:
            logging.error("Authentication failed (401). Check your .env file and ensure your system clock is synchronized.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching data for {pair}: {e}")
        return None