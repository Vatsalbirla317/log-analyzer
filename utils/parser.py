import json
import pandas as pd
import re

def parse_log_file(filepath):
    try:
        if filepath.endswith(".json"):
            with open(filepath, "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        else:
            # Read and parse each log line using regex
            log_entries = []
            pattern = r'^(INFO|ERROR|WARNING)\s+([^\s]+)\s+([^\s]+)\s+(.+)$'

            with open(filepath, "r") as f:
                for line in f:
                    match = re.match(pattern, line.strip())
                    if match:
                        level, timestamp, service, message = match.groups()
                        log_entries.append({
                            "timestamp": timestamp,
                            "service": service,
                            "level": level,
                            "message": message
                        })

            df = pd.DataFrame(log_entries)

        # Defensive check
        required_cols = {"timestamp", "service", "level", "message"}
        if not required_cols.issubset(set(df.columns)):
            return pd.DataFrame(columns=list(required_cols))

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df.dropna(subset=["timestamp"])

    except Exception as e:
        print(f"[Parser Error] {e}")
        return pd.DataFrame(columns=["timestamp", "service", "level", "message"])

