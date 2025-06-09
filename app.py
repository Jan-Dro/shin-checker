from flask import Flask
from checker import run_check
import threading
import time
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>🌱 Shin Deshojo Checker is running hourly in the background!</h2>"

@app.route("/check")
def manual_check():
    run_check()
    return "✅ Manual check complete — email sent if in stock."

def hourly_checker():
    while True:
        print("🔁 Hourly check triggered...")
        run_check()
        time.sleep(3600) 

if __name__ == "__main__":
    checker_thread = threading.Thread(target=hourly_checker, daemon=True)
    checker_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
