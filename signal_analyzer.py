import numpy as np

def _calculate_ema(prices, period):
    """Helper to calculate Exponential Moving Average."""
    # Find the start index of the first valid number
    start_idx_arr = np.where(~np.isnan(prices))[0]
    if len(start_idx_arr) == 0:
        return np.full_like(prices, np.nan)
    
    start_idx = start_idx_arr[0]
    
    if len(prices) < start_idx + period:
        return np.full_like(prices, np.nan)
    
    ema = np.full_like(prices, np.nan)
    
    # The first EMA is a simple moving average
    first_ema_idx = start_idx + period - 1
    ema[first_ema_idx] = np.mean(prices[start_idx : first_ema_idx + 1])

    # Multiplier for smoothing
    multiplier = 2 / (period + 1)
    # Calculate the rest of the EMAs
    for i in range(first_ema_idx + 1, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]
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

def detect_patterns(ohlc_data):
    """
    Detects candlestick patterns. Focuses on Bullish and Bearish Engulfing.
    Accepts a numpy array of OHLC data.
    Returns a list of tuples: (pattern_name, candle_index).
    """
    patterns = []
    if len(ohlc_data) < 2: # Need at least 2 candles for pattern comparison
        return patterns

    for i in range(1, len(ohlc_data)):
        # ohlc_data format: [open, high, low, close]
        prev_o, _, _, prev_c = ohlc_data[i-1]
        curr_o, curr_h, curr_l, curr_c = ohlc_data[i]

        # Bullish Engulfing
        if (prev_c < prev_o) and (curr_c > curr_o) and \
           (curr_c > prev_o and curr_o < prev_c):
            patterns.append(("Bullish Engulfing", i))

        # Bearish Engulfing
        elif (prev_c > prev_o) and (curr_c < curr_o) and \
             (curr_c < prev_o and curr_o > prev_c):
            patterns.append(("Bearish Engulfing", i))

        # Hammer and Hanging Man detection
        body = abs(curr_c - curr_o)
        if body > 0: # Avoid division by zero for doji-like candles
            upper_shadow = curr_h - max(curr_o, curr_c)
            lower_shadow = min(curr_o, curr_c) - curr_l
            is_hammer_shape = lower_shadow >= 2 * body and upper_shadow <= 0.5 * body

            # Hammer (bullish reversal after downtrend)
            if is_hammer_shape and prev_c < prev_o:
                patterns.append(("Hammer", i))
            
            # Hanging Man (bearish reversal after uptrend)
            elif is_hammer_shape and prev_c > prev_o:
                patterns.append(("Hanging Man", i))

    return patterns

def _get_signal_direction_from_components(components):
    """Determines signal direction (Buy/Sell/Watch) from signal components."""
    if 'ema_cross' in components and 'Golden' in components['ema_cross']: return 'Buy'
    if 'pattern_detected' in components and 'Bullish' in components['pattern_detected']: return 'Buy'
    if 'macd_cross' in components and 'Bullish' in components['macd_cross']: return 'Buy'
    if 'pattern_detected' in components and 'Hammer' in components['pattern_detected']: return 'Buy'
    
    if 'ema_cross' in components and 'Death' in components['ema_cross']: return 'Sell'
    if 'pattern_detected' in components and 'Bearish' in components['pattern_detected']: return 'Sell'
    if 'macd_cross' in components and 'Bearish' in components['macd_cross']: return 'Sell'
    if 'pattern_detected' in components and 'Hanging Man' in components['pattern_detected']: return 'Sell'

    return 'Watch'

def calculate_confidence(signal_components, rsi_value):
    """
    Calculates an advanced confidence score based on the confluence of signals.
    This model uses both base weights and confluence bonuses.
    """
    score = 0
    base_weights = {
        "pattern": 40,
        "ema_cross": 60,
        "bollinger_cross": 15,
        "macd_cross": 25,
        "rsi_cross": 20,
    }
    confluence_bonus = {
        "trend_momentum": 25,  # EMA Cross + MACD Cross
        "volatility_reversal": 20, # Bollinger Cross + RSI Cross
        "pattern_confirmation": 15 # Pattern + another signal
    }

    # --- Calculate base score from individual signals ---
    has_pattern = 'pattern_detected' in signal_components
    has_ema_cross = 'ema_cross' in signal_components
    has_bollinger_cross = 'bollinger_cross' in signal_components
    has_macd_cross = 'macd_cross' in signal_components
    has_rsi_cross = 'rsi_cross' in signal_components

    if has_pattern: score += base_weights["pattern"]
    if has_ema_cross: score += base_weights["ema_cross"]
    if has_bollinger_cross: score += base_weights["bollinger_cross"]
    if has_macd_cross: score += base_weights["macd_cross"]
    if has_rsi_cross: score += base_weights["rsi_cross"]

    # --- Add confluence bonuses for powerful combinations ---
    direction = _get_signal_direction_from_components(signal_components)

    # Bonus 1: Trend (EMA) + Momentum (MACD)
    if has_ema_cross and has_macd_cross:
        is_bullish_ema = 'Golden' in signal_components['ema_cross']
        is_bullish_macd = 'Bullish' in signal_components['macd_cross']
        is_bearish_ema = 'Death' in signal_components['ema_cross']
        is_bearish_macd = 'Bearish' in signal_components['macd_cross']
        if (is_bullish_ema and is_bullish_macd) or (is_bearish_ema and is_bearish_macd):
            score += confluence_bonus["trend_momentum"]

    # Bonus 2: Volatility (Bollinger) + Momentum (RSI)
    if has_bollinger_cross and has_rsi_cross:
        is_lower_bband = 'Lower' in signal_components['bollinger_cross']
        is_oversold_rsi = 'Oversold' in signal_components['rsi_cross']
        is_upper_bband = 'Upper' in signal_components['bollinger_cross']
        is_overbought_rsi = 'Overbought' in signal_components['rsi_cross']
        if (is_lower_bband and is_oversold_rsi) or (is_upper_bband and is_overbought_rsi):
            score += confluence_bonus["volatility_reversal"]

    # Bonus 3: Candlestick Pattern confirmed by another indicator
    if has_pattern:
        num_other_signals = len([k for k in signal_components if k != 'pattern_detected'])
        if num_other_signals > 0:
            score += confluence_bonus["pattern_confirmation"]

    # --- Final RSI confirmation check (similar to before) ---
    if not np.isnan(rsi_value):
        # If we have a directional signal (buy/sell), check if RSI confirms it.
        if direction == 'Buy' and rsi_value > 50 and rsi_value < 70:
            score += 20 # Add a stronger, final confirmation bonus
        elif direction == 'Sell' and rsi_value < 50 and rsi_value > 30:
            score += 20

    return min(int(score), 100)

def calculate_macd(closes, fast_period=12, slow_period=26, signal_period=9):
    """Calculates MACD, Signal Line, and Histogram."""
    if len(closes) < slow_period:
        return (np.full_like(closes, np.nan),
                np.full_like(closes, np.nan),
                np.full_like(closes, np.nan))

    ema_fast = _calculate_ema(closes, fast_period)
    ema_slow = _calculate_ema(closes, slow_period)
    macd_line = ema_fast - ema_slow
    signal_line = _calculate_ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(closes, period=20, std_dev=2):
    """Calculates Bollinger Bands."""
    if len(closes) < period:
        return (np.full_like(closes, np.nan),
                np.full_like(closes, np.nan),
                np.full_like(closes, np.nan))
    
    sma = np.convolve(closes, np.ones(period), 'valid') / period
    std = np.array([np.std(closes[i:i+period]) for i in range(len(closes) - period + 1)])
    
    middle_band = np.concatenate((np.full(period - 1, np.nan), sma))
    upper_band = np.concatenate((np.full(period - 1, np.nan), sma + (std * std_dev)))
    lower_band = np.concatenate((np.full(period - 1, np.nan), sma - (std * std_dev)))
    
    return upper_band, middle_band, lower_band

def analyze_signals(candles, evaluate_confidence=False, return_all=False):
    signals = []
    # --- Use standard, less noisy EMA periods for trend analysis ---
    short_period = 50
    long_period = 200 # Use the longest period to determine where analysis can start
    
    if len(candles) < long_period:
        # Not enough data to calculate the long-term EMA, so we can't analyze.
        return []

    # Convert candle data to numpy array for efficient processing
    # Assumes candle format: [timestamp, open, high, low, close, volume]
    ohlc_data = np.array([[float(c[1]), float(c[2]), float(c[3]), float(c[4])] for c in candles])
    closes = ohlc_data[:, 3]

    # --- Calculate all indicators for the entire series ---
    all_rsi_values = calculate_rsi(closes)
    ema_short = _calculate_ema(closes, short_period)
    ema_long = _calculate_ema(closes, long_period)
    macd_line, signal_line, macd_histogram = calculate_macd(closes)
    upper_band, _, lower_band = calculate_bollinger_bands(closes)
    # Create a lookup dictionary for patterns for efficient access
    patterns_by_index = {index: name for name, index in detect_patterns(ohlc_data)}

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
            signal_components['ema_cross'] = "Golden Cross (50/200)"
            reasons.append("Golden Cross (EMA 50/200)")
        elif ema_short[i-1] >= ema_long[i-1] and ema_short[i] < ema_long[i]:
            signal_components['ema_cross'] = "Death Cross (50/200)"
            reasons.append("Death Cross (EMA 50/200)")

        # 3. Check for MACD Crossover
        if not np.isnan(macd_line[i]) and not np.isnan(signal_line[i]):
            if macd_line[i-1] <= signal_line[i-1] and macd_line[i] > signal_line[i]:
                signal_components['macd_cross'] = 'Bullish'
                reasons.append("MACD Bullish Cross")
            elif macd_line[i-1] >= signal_line[i-1] and macd_line[i] < signal_line[i]:
                signal_components['macd_cross'] = 'Bearish'
                reasons.append("MACD Bearish Cross")

        # 4. Check for Bollinger Band Crossover
        if not np.isnan(closes[i]) and not np.isnan(upper_band[i]) and not np.isnan(lower_band[i]):
            if closes[i-1] <= upper_band[i-1] and closes[i] > upper_band[i]:
                signal_components['bollinger_cross'] = 'Upper'
                reasons.append("Price broke upper Bollinger Band")
            elif closes[i-1] >= lower_band[i-1] and closes[i] < lower_band[i]:
                signal_components['bollinger_cross'] = 'Lower'
                reasons.append("Price broke lower Bollinger Band")

        # 5. Check for RSI Threshold Crossing Event
        rsi_now = all_rsi_values[i]
        rsi_prev = all_rsi_values[i-1]
        if not np.isnan(rsi_now) and not np.isnan(rsi_prev):
            if rsi_prev >= 30 and rsi_now < 30:
                reason_str = f"RSI crossed into Oversold ({round(rsi_now, 2)})"
                reasons.append(reason_str)
                signal_components['rsi_cross'] = 'Oversold'
            elif rsi_prev <= 70 and rsi_now > 70:
                reason_str = f"RSI crossed into Overbought ({round(rsi_now, 2)})"
                reasons.append(reason_str)
                signal_components['rsi_cross'] = 'Overbought'

        # --- If any event was found, build and log the signal ---
        if reasons:
            rsi_at_signal = round(all_rsi_values[i], 2) if not np.isnan(all_rsi_values[i]) else np.nan
            signal_type = _get_signal_direction_from_components(signal_components)

            signal = {
                "timestamp": candles[i][0],
                "signal_type": signal_type,
                "pattern_detected": signal_components.get('pattern_detected', 'N/A'),
                "rsi": rsi_at_signal if not np.isnan(rsi_at_signal) else "N/A",
                "ema_cross": signal_components.get('ema_cross', 'N/A'),
                "macd": round(macd_histogram[i], 2) if not np.isnan(macd_histogram[i]) else "N/A",
                "reason": ", ".join(reasons)
            }

            if evaluate_confidence:
                confidence_score = calculate_confidence(signal_components, rsi_at_signal)
                signal['confidence'] = confidence_score

            signals.append(signal)

    # Return only the most recent signals to avoid historical noise.
    # For example, return the last 5 signals found.
    if return_all:
        return signals
    return signals[-5:]