import pandas as pd

def detect_anomalies(df):
    # Count errors per service
    error_counts = df[df['level'] == 'ERROR'].groupby('service').size().reset_index(name='error_count')

    # Define threshold (e.g., any service with >= 2 errors is abnormal)
    threshold = 2
    anomalies = error_counts[error_counts['error_count'] >= threshold]

    anomalies['anomaly'] = -1  # mark as anomaly like IsolationForest
    anomalies['dummy'] = 1     # for consistency with previous format
    return anomalies
