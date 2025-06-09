from flask import Flask
from checker import run_check
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)
check_log = []

@app.route("/")
def home():
    return "<h2>🌱 Shin Deshojo Checker is running every hour with daily summary!</h2>"

@app.route("/check")
def manual_check():
    result = run_check()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    check_log.append(f"[{timestamp}] Manual Check:\n{result}")
    return "✅ Manual check complete."

def hourly_checker():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"🔁 Hourly check at {timestamp}")
        result = run_check()
        check_log.append(f"[{timestamp}]\n{result}")
        time.sleep(3600)

def daily_summary():
    while True:
        now = datetime.now()
        if now.hour == 7 and now.minute == 0:
            print("📬 Sending daily summary...")
            summary = "<h3>🌿 Daily Shin Deshojo Summary</h3><pre>" + "\n\n".join(check_log[-24:]) + "</pre>"
            send_email("🌿 Daily Maple Stock Summary", summary)
            time.sleep(60)
        time.sleep(30)

def send_email(subject, body):
    import requests
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
    print("✅ Daily email sent!" if res.status_code == 200 else f"❌ Email failed: {res.text}")

if __name__ == "__main__":
    threading.Thread(target=hourly_checker, daemon=True).start()
    threading.Thread(target=daily_summary, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
