"""
The Sage — processes indicators and conjures buy/sell signals.
"""
import logging
from typing import Optional, Tuple

import pandas as pd
import pandas_ta as ta

import config


def generate_signals(df: pd.DataFrame) -> Tuple[Optional[str], pd.DataFrame]:
    """
    Processes candlestick data to generate trading signals based on SMA and RSI.

    Args:
        df (pd.DataFrame): DataFrame with candlestick data. Must contain
                           'open', 'high', 'low', 'close', 'volume' columns.

    Returns:
        Tuple[Optional[str], pd.DataFrame]: A tuple containing the signal
                                            ("BUY", "SELL", or "HOLD") and the
                                            DataFrame with appended indicator columns.
                                            Returns (None, df) if not enough data.
    """
    if df is None or len(df) < config.SMA_LONG_PERIOD:
        # Not enough data to compute the long SMA, so no signal can be generated.
        logging.warning(
            f"Not enough data to generate signals. Have {len(df) if df is not None else 0} candles, need {config.SMA_LONG_PERIOD}."
        )
        return None, df

    # --- Calculate Indicators ---
    # The 'ta' extension is added to the DataFrame by pandas_ta.
    df.ta.sma(length=config.SMA_SHORT_PERIOD, append=True)
    df.ta.sma(length=config.SMA_LONG_PERIOD, append=True)
    df.ta.rsi(length=config.RSI_PERIOD, append=True)

    # Clean up column names for easier access. pandas_ta creates names like 'SMA_12'.
    sma_short_col = f"SMA_{config.SMA_SHORT_PERIOD}"
    sma_long_col = f"SMA_{config.SMA_LONG_PERIOD}"
    rsi_col = f"RSI_{config.RSI_PERIOD}"

    # --- Generate Signals ---
    # We look at the latest full candle to determine the signal.
    latest = df.iloc[-1]

    # RSI Logic: Overbought/Oversold are strong signals.
    if latest[rsi_col] < config.RSI_OVERSOLD_THRESHOLD:
        return "BUY", df
    if latest[rsi_col] > config.RSI_OVERBOUGHT_THRESHOLD:
        return "SELL", df

    # SMA Crossover Logic
    # Golden Cross (Buy Signal): Short-term SMA crosses above long-term SMA.
    if df.iloc[-2][sma_short_col] < df.iloc[-2][sma_long_col] and latest[sma_short_col] > latest[sma_long_col]:
        return "BUY", df
    # Death Cross (Sell Signal): Short-term SMA crosses below long-term SMA.
    if df.iloc[-2][sma_short_col] > df.iloc[-2][sma_long_col] and latest[sma_short_col] < latest[sma_long_col]:
        return "SELL", df

    return "HOLD", df