import sqlite3
import pandas as pd

def init_db(db_name="log_storage.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            timestamp TEXT,
            level TEXT,
            service TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_logs(df, db_name="log_storage.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("logs", conn, if_exists="append", index=False)
    conn.close()

def fetch_logs(db_name="log_storage.db"):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()
    return df
