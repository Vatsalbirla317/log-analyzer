import json
import pandas as pd
import re
import os

def parse_log_file(filepath):
    try:
        if not os.path.exists(filepath):
            print(f"[Parser Error] File does not exist: {filepath}")
            return pd.DataFrame(columns=["timestamp", "service", "level", "message"])

        ext = os.path.splitext(filepath)[1].lower()

        if ext == ".json":
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                df = pd.DataFrame(data)
            else:
                print("[Parser Error] JSON must be a list of dictionaries.")
                return pd.DataFrame(columns=["timestamp", "service", "level", "message"])

        elif ext == ".log":
            log_entries = []
            # Supports: LEVEL TIMESTAMP SERVICE MESSAGE (flexible spacing)
            pattern = r'^(INFO|ERROR|WARNING)\s+([\d\-T:\s]+)\s+([^\s]+)\s+(.+)$'
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    match = re.match(pattern, line)
                    if match:
                        level, timestamp, service, message = match.groups()
                        log_entries.append({
                            "timestamp": timestamp.strip(),
                            "service": service.strip(),
                            "level": level.strip(),
                            "message": message.strip()
                        })
            df = pd.DataFrame(log_entries)

        else:
            print("[Parser Error] Unsupported file format. Must be .log or .json")
            return pd.DataFrame(columns=["timestamp", "service", "level", "message"])

        # Verify required columns
        required_cols = {"timestamp", "service", "level", "message"}
        if not required_cols.issubset(df.columns):
            print("[Parser Error] Missing required columns")
            return pd.DataFrame(columns=list(required_cols))

        # Convert timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Drop invalid datetime entries
        return df.dropna(subset=["timestamp"]).reset_index(drop=True)

    except Exception as e:
        print(f"[Parser Error] {e}")
        return pd.DataFrame(columns=["timestamp", "service", "level", "message"])
