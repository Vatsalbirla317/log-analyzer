import json
import pandas as pd
import re
from datetime import datetime

def parse_log_file(filepath):
    try:
        if filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                df = pd.DataFrame(data)
            else:
                print("[Parser Error] JSON must be a list of log entries")
                return pd.DataFrame(columns=["timestamp", "service", "level", "message"])

        else:  # .log file
            log_entries = []
            skipped = 0

            # Define multiple known patterns
            patterns = [
                r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+)\s+(.+)$',                     # timestamp service level msg
                r'^(INFO|ERROR|WARNING|DEBUG)\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(.+)$', # level timestamp service msg
                r'^(\w+)\s+(INFO|ERROR|WARNING|DEBUG)\s+(.+)$',                                        # service level msg (no timestamp)
            ]

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if len(line) > 5000:
                        continue  # skip unusually long lines

                    matched = False

                    for pattern in patterns:
                        match = re.match(pattern, line)
                        if match:
                            groups = match.groups()
                            if len(groups) == 4:
                                if pattern.startswith('^('):  # timestamp first
                                    timestamp, service, level, message = groups
                                else:  # level first
                                    level, timestamp, service, message = groups
                            elif len(groups) == 3:  # no timestamp
                                service, level, message = groups
                                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                            log_entries.append({
                                "timestamp": timestamp,
                                "service": service,
                                "level": level.upper(),
                                "message": message
                            })
                            matched = True
                            break

                    if not matched:
                        skipped += 1
                        if skipped <= 10:
                            print(f"[Warning] Line {i} didn't match any known format:\n{line[:120]}")

            print(f"[Parser] Parsed {len(log_entries)} entries | Skipped {skipped} lines")
            df = pd.DataFrame(log_entries)

        # Final cleaning
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        df = df[["timestamp", "service", "level", "message"]]

        return df

    except Exception as e:
        print(f"[Parser Error] {e}")
        return pd.DataFrame(columns=["timestamp", "service", "level", "message"])
