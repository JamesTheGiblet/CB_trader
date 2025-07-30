import numpy as np

def _calculate_ema(prices, period):
    """Helper to calculate Exponential Moving Average."""
    if len(prices) < period:
        return np.full_like(prices, np.nan)
    # The first EMA is a simple moving average
    ema = np.zeros_like(prices, dtype=float)
    ema[period-1] = np.mean(prices[:period])
    # Multiplier for smoothing
    multiplier = 2 / (period + 1)
    # Calculate the rest of the EMAs
    for i in range(period, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]
    ema[:period-1] = np.nan # Set initial values to NaN
    return ema

def calculate_rsi(closes, period=14):
    """
    Calculates RSI for a full series of close prices using Wilder's smoothing.
    Returns an array of RSI values corresponding to each candle.
    """
    if len(closes) <= period:
        return np.full(len(closes), np.nan)

    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    # Use Wilder's smoothing for RSI
    avg_gain = np.zeros_like(closes)
    avg_loss = np.zeros_like(closes)
    
    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])

    for i in range(period + 1, len(closes)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gains[i-1]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + losses[i-1]) / period

    rs = np.divide(avg_gain, avg_loss, out=np.full_like(avg_gain, np.inf), where=avg_loss!=0)
    rsi = 100 - (100 / (1 + rs))
    rsi[:period] = np.nan # Set initial values to NaN
    return rsi

def detect_patterns(candles):
    """
    Detects candlestick patterns. Focuses on Bullish and Bearish Engulfing.
    Returns a list of tuples: (pattern_name, candle_index).
    """
    patterns = []
    if len(candles) < 2:
        return patterns

    for i in range(1, len(candles)):
        # Assumes candle format: [timestamp, open, high, low, close, volume]
        prev_open, prev_close = float(candles[i-1][1]), float(candles[i-1][4])
        curr_open, curr_close = float(candles[i][1]), float(candles[i][4])

        # Bullish Engulfing
        if (prev_close < prev_open) and (curr_close > curr_open) and \
           (curr_close > prev_open and curr_open < prev_close):
            patterns.append(("Bullish Engulfing", i))

        # Bearish Engulfing
        elif (prev_close > prev_open) and (curr_close < curr_open) and \
             (curr_close < prev_open and curr_open > prev_close):
            patterns.append(("Bearish Engulfing", i))
            
    return patterns

def analyze_signals(candles):
    signals = []
    long_period = 20 # Use the longest period to determine where analysis can start
    closes = np.array([float(c[4]) for c in candles])
    
    if len(closes) < long_period:
        return []

    # --- Calculate all indicators for the entire series ---
    all_rsi_values = calculate_rsi(closes)
    ema_short = _calculate_ema(closes, 5)
    ema_long = _calculate_ema(closes, long_period)
    # Create a lookup dictionary for patterns for efficient access
    patterns_by_index = {index: name for name, index in detect_patterns(candles)}

    # --- Iterate through candles to find signal events ---
    for i in range(long_period, len(candles)):
        reasons = []
        signal_components = {}

        # 1. Check for Candlestick Pattern
        if i in patterns_by_index:
            pattern = patterns_by_index[i]
            signal_components['pattern_detected'] = pattern
            reasons.append(pattern)

        # 2. Check for EMA Cross Event
        if ema_short[i-1] <= ema_long[i-1] and ema_short[i] > ema_long[i]:
            signal_components['ema_cross'] = "Golden Cross"
            reasons.append("Golden Cross (EMA 5/20)")
        elif ema_short[i-1] >= ema_long[i-1] and ema_short[i] < ema_long[i]:
            signal_components['ema_cross'] = "Death Cross"
            reasons.append("Death Cross (EMA 5/20)")

        # 3. Check for RSI Threshold Crossing Event
        rsi_now = all_rsi_values[i]
        rsi_prev = all_rsi_values[i-1]
        if not np.isnan(rsi_now) and not np.isnan(rsi_prev):
            if rsi_prev >= 30 and rsi_now < 30:
                reasons.append(f"RSI crossed into Oversold ({round(rsi_now, 2)})")
            elif rsi_prev <= 70 and rsi_now > 70:
                reasons.append(f"RSI crossed into Overbought ({round(rsi_now, 2)})")

        # --- If any event was found, build and log the signal ---
        if reasons:
            rsi_at_signal = round(all_rsi_values[i], 2) if not np.isnan(all_rsi_values[i]) else "N/A"
            signal_type = "Buy" if "Golden" in " ".join(reasons) or "Bullish" in " ".join(reasons) else \
                          "Sell" if "Death" in " ".join(reasons) or "Bearish" in " ".join(reasons) else "Watch"

    return signals