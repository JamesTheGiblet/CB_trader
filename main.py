"""
The High Priest — orchestrates signal summons and terminal display.
"""
import logging
from dotenv import load_dotenv
import time
import analysis
import config
import coinbase_api
import database
import utils

def process_pair(pair: str):
    """
    Performs the full ritual for a single trading pair:
    Fetch -> Inscribe -> Analyze -> Report.
    """
    logging.info(f"Processing pair: {pair}")
    df = coinbase_api.fetch_candlestick_data(pair)

    if df is not None:
        logging.info(f"Fetched {len(df)} candlesticks for {pair}. Inscribing to the scrolls...")
        database.save_candlestick_data(pair, df)

        # Invoke the Sage to analyze the scrolls
        logging.info(f"Invoking the signal spirits for {pair}...")
        signal, analyzed_df = analysis.generate_signals(df.copy()) # Use a copy for analysis

        if signal and not analyzed_df.empty:
            logging.info(f"Signal Generated: {signal} for {pair}.")
            utils.display_oracle_verdict(pair, signal, analyzed_df)
        else:
            logging.warning(f"The spirits need more data for {pair} to form a vision. No signal generated.")

    else:
        logging.error(f"Fetch failed for {pair}. The spirits are silent.")

def main():
    """The main ritual."""
    load_dotenv()  # Load environment variables from .env file
    utils.setup_logging()
    logging.info("CB_Trader awakens...")
 
    # First, sanctify the database to ensure our scrolls are ready.
    database.init_db()
 
    try:
        while True:
            logging.info("--- Starting new divination cycle ---")
            for pair in config.TRACKED_PAIRS:
                process_pair(pair)
                time.sleep(2) # A small courtesy pause between pairs
            logging.info(f"Cycle complete. The oracle will rest for {config.POLLING_INTERVAL_SECONDS} seconds...")
            time.sleep(config.POLLING_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("\nThe oracle is commanded to rest. Shutting down gracefully.")
 
if __name__ == "__main__":
    main()