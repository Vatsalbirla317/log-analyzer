from utils.parser import parse_log_file
from utils.anomaly import detect_anomalies

LOG_FILE = 'logs/sample1.log'

def main():
    print(f"Parsing log file: {LOG_FILE}")
    df = parse_log_file(LOG_FILE)
    print("\nParsed Logs:")
    print(df)

    print("\nRunning anomaly detection...")
    anomalies = detect_anomalies(df)
    print("\nAnomalous services:")
    print(anomalies)

if __name__ == "__main__":
    main()
