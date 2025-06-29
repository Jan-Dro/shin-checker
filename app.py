from flask import Flask
from checker import run_check
import threading
import time
import os
from datetime import datetime
import requests
import pytz

app = Flask(__name__)
log = []

@app.route("/")
def home():
    """Landing page for the checker."""
    return "<h2>Shin Deshojo Checker is running every hour with daily summary!</h2>"

@app.route("/check")
def manual_check():
    # Run a manual check and log the result
    results = run_check()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log.append(f"[{timestamp}] Manual Check:\n{results}")
    return "Manual check complete."

def hourly_checker():
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            print(f"Hourly check at {timestamp}")
            results = run_check()
            log.append(f"[{timestamp}]\n{results}")
        except Exception as e:
            print(f"Hourly check failed: {e}")
        time.sleep(3600)

def daily_summary():
    cst = pytz.timezone("America/Chicago")
    while True:
        now = datetime.now(cst)
        if (now.hour == 8 or now.hour == 20) and now.minute == 0:
            try:
                print("Sending daily summary...")
                summary = "<h3>Daily Shin Deshojo Summary</h3><pre>" + "\n\n".join(log[-24:]) + "</pre>"
                send_email("Daily Maple Stock Summary", summary)
            except Exception as e:
                print(f"Failed to send daily summary: {e}")
            time.sleep(60)
        time.sleep(30)

def send_email(subject, body):
    """Send an email using the Resend API."""
    headers = {
        "Authorization": f"Bearer {os.environ.get('RESEND_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "from": os.environ.get("EMAIL_FROM"),
        "to": [os.environ.get("EMAIL_TO")],
        "subject": subject,
        "html": f"<pre>{body}</pre>"
    }
    res = requests.post("https://api.resend.com/emails", headers=headers, json=data)
    if res.status_code == 200:
        print("Daily email sent!")
    else:
        print(f"Email failed: {res.text}")

if __name__ == "__main__":
    # Start background threads for hourly and daily checks
    threading.Thread(target=hourly_checker, daemon=True).start()
    threading.Thread(target=daily_summary, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)