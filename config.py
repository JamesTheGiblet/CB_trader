"""
The Codex — holds your divine preferences.
"""
import os
import json

# --- Environment Selector ---
# Set to True to use Sandbox keys and URLs, False for production.
# NOTE: With JWT authentication, the API endpoint is the same for both.
# The API Key itself determines if the request hits sandbox or production.
SANDBOX_MODE = True

# --- Sacred Scrolls (API Key File) ---
# Your Coinbase API Key Name and Private Key, read from cdp_api_key.json.
# These are required for the Messenger to commune with the Coinbase spirits.
API_KEY_NAME = None
API_PRIVATE_KEY = None

try:
    with open("cdp_api_key.json", "r") as f:
        api_key_data = json.load(f)
        API_KEY_NAME = api_key_data.get("name")
        API_PRIVATE_KEY = api_key_data.get("privateKey")
except (FileNotFoundError, json.JSONDecodeError, KeyError):
    # This will be handled more gracefully in coinbase_api.py before requests
    pass
# --- Divination Preferences ---

# The canonical pairs to watch. Add or remove as you see fit.
# Format: "PRODUCT-CURRENCY" (e.g., "BTC-USD")
TRACKED_PAIRS = [
    "BTC-USD",
    "ETH-USD",
    "XRP-USD",
    "USDT-USD",
    # NOTE: BNB is not available on the standard Coinbase API for all regions.
    # We'll substitute with Solana (SOL) as a modern, high-volume alternative.
    "SOL-USD",
]

# The time in seconds the High Priest waits before seeking new whispers.
POLLING_INTERVAL_SECONDS = 300  # 5 minutes

# --- Signal Incantations (Technical Analysis Parameters) ---

SMA_SHORT_PERIOD = 12  # Simple Moving Average (short-term)
SMA_LONG_PERIOD = 26   # Simple Moving Average (long-term)
RSI_PERIOD = 14        # Relative Strength Index
RSI_OVERBOUGHT_THRESHOLD = 70
RSI_OVERSOLD_THRESHOLD = 30