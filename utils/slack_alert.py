import requests
import json

def send_slack_alert(services, webhook_url):
    message = {
        "text": f"🚨 Anomaly spike detected in: {', '.join(services)}"
    }
    response = requests.post(webhook_url, data=json.dumps(message),
                             headers={"Content-Type": "application/json"})
    return response.status_code == 200
