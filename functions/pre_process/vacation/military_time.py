from datetime import datetime

def standardize_time(timestamp: datetime) -> datetime:
    """
    Convert 1-3 AM times to PM format (adds 12 hours).
    
    Args:
        timestamp: A datetime object to standardize
        
    Returns:
        datetime: The standardized datetime object
    """
    if timestamp and 1 <= timestamp.hour <= 3:
        return timestamp.replace(hour=timestamp.hour + 12)
    return timestamp
