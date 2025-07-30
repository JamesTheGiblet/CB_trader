"""
This module provides the "Mythic Flair" for CB_Trader, translating technical
signals into thematic, poetic tags.
"""

def get_mythic_tag(signal_type: str, confidence: int, reason: str) -> str:
    """
    Generates a mythic tag based on signal characteristics.

    Args:
        signal_type (str): The type of signal ('Buy', 'Sell', 'Watch').
        confidence (int): The confidence score of the signal (0-100).
        reason (str): The technical reason for the signal.

    Returns:
        str: A poetic, mythic tag.
    """
    if "Golden Cross" in reason:
        return "The Phoenix Rises" if confidence >= 80 else "A Glimmer of Gold"
    
    if "Death Cross" in reason:
        return "The Serpent's Shadow" if confidence >= 80 else "A Whisper of Winter"

    if "MACD Bullish Cross" in reason:
        return "The Tide Turns"
    
    if "MACD Bearish Cross" in reason:
        return "An Ebbing Current"

    if "upper Bollinger" in reason:
        return "Touching the Sun"
        
    if "lower Bollinger" in reason:
        return "River of Shadows"

    if "Hammer" in reason:
        return "The Smith's Anvil"

    if "Hanging Man" in reason:
        return "A Frayed Thread"

    if "Bullish Engulfing" in reason:
        return "The Bull's Embrace"

    if "Bearish Engulfing" in reason:
        return "The Bear's Grasp"

    if "Oversold" in reason:
        return "Echoes from the Depths"
    
    if "Overbought" in reason:
        return "Whispers from the Peak"

    return "The Oracle is Silent"