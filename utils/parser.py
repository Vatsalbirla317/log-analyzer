import json
import pandas as pd

def parse_log_file(filepath):
    try:
        if filepath.endswith(".json"):
            with open(filepath, "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        else:
            df = pd.read_csv(
                filepath,
                sep=" - ",
                header=None,
                names=["timestamp", "service", "level", "message"],
                engine="python"
            )

        # Defensive check
        required_cols = {"timestamp", "service", "level", "message"}
        if not required_cols.issubset(set(df.columns)):
            return pd.DataFrame(columns=list(required_cols))

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    except Exception as e:
        print(f"[Parser Error] {e}")
        return pd.DataFrame(columns=["timestamp", "service", "level", "message"])
