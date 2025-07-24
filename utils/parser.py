import re
import pandas as pd

def parse_log_file(filepath):
    logs = []
    pattern = r'(\w+)\s+(\d{4}-\d{2}-\d{2}T[\d:]+Z)\s+(\w+)\s+(.*)'

    with open(filepath, 'r') as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                level, timestamp, service, message = match.groups()
                logs.append({
                    "timestamp": timestamp,
                    "level": level,
                    "service": service,
                    "message": message
                })
    
    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
