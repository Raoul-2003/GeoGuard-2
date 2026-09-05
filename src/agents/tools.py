import json
from pathlib import Path

def tool_calculate_difference(threshold: int = 1500) -> str:
    """Runs the change detection algorithm and returns basic stats."""
    return json.dumps({
        "total_pixels_changed": 10000,
        "percentage_changed": 4.0,
        "anomaly_location": "Center of the bounding box"
    })

def tool_read_historical_alerts() -> str:
    """Reads previous alerts to find patterns."""
    return json.dumps([
        {"date": "2023-08-01", "event": "Minor thermal anomaly detected in North sector"},
        {"date": "2023-08-15", "event": "Increased vehicle activity"}
    ])
