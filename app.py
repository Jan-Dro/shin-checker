from flask import Flask
from checker import run_check
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>🌱 Shin Deshojo Checker is live on Render!</h2><p>Visit <a href='/check'>/check</a> to run a stock check.</p>"

@app.route("/check")
def check_now():
    run_check()
    return "✅ Check complete — email sent if stock is available."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
