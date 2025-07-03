def standardize_time(timestamp):
    """
    Convert 12-hour format afternoon times (1-5 PM) to 24-hour format (13-17).

    Args:
        timestamp (datetime): A datetime object with potentially non-standardized hours

    Returns:
        datetime: The timestamp with standardized 24-hour time format
    """
    if timestamp is None:
        raise ValueError("Timestamp cannot be None")

    # Convert afternoon hours 24-hour format
    if 1 <= timestamp.hour <= 5:
        return timestamp.replace(hour=timestamp.hour + 12)
    return timestamp
