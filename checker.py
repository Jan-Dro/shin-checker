import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

PRODUCTS = {
    "Maplestone": "https://maplestoneornamentals.com/products/shin-deshojo?variant=41617087103072",
    "MrMaple": "https://mrmaple.com/products/buy-acer-palmatum-shin-deshojo-red-japanese-maple?variant=46355750617315"
}

def is_in_stock(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return "sold out" not in soup.text.lower()

def send_email(subject, body):
    res = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer " + RESEND_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "from": EMAIL_FROM,
            "to": [EMAIL_TO],
            "subject": subject,
            "html": body
        }
    )
    print("✅ Email sent!" if res.status_code == 200 else f"❌ Email failed: {res.text}")

def run_check():
    print("🌱 Checking Shin Deshojo availability...")
    any_in_stock = False
    html_body = "<h3>Shin Deshojo In Stock!</h3><ul>"

    for name, url in PRODUCTS.items():
        try:
            if is_in_stock(url):
                any_in_stock = True
                html_body += f"<li><a href='{url}'>{name} is in stock</a></li>"
                print(f"✅ {name} is in stock!")
            else:
                print(f"❌ {name} is sold out.")
        except Exception as e:
            print(f"⚠️ Error checking {name}: {e}")

    html_body += "</ul>"

    if any_in_stock:
        send_email("🌱 Shin Deshojo Available!", html_body)
