import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

PRODUCTS = {
    "Maplestone Shin Deshojo" : ["https://maplestoneornamentals.com/products/shin-deshojo?variant=41617087103072", "https://maplestoneornamentals.com/products/shin-deshojo?variant=40052844363872"],
    "Maplestone Deshojo": "https://maplestoneornamentals.com/products/deshojo?_pos=1&_sid=b0a23f88c&_ss=r",
    "MrMaple Shin Deshojo": ["https://mrmaple.com/products/buy-acer-palmatum-shin-deshojo-red-japanese-maple?variant=46355750617315","https://mrmaple.com/collections/weeklywhammy/products/buy-acer-palmatum-shin-deshojo-red-japanese-maple","https://mrmaple.com/collections/weeklywhammy/products/buy-acer-palmatum-shin-deshojo-red-japanese-maple?variant=32445571956811"],
    "MrMaple Deshojo": ["https://mrmaple.com/products/buy-acer-palmatum-deshojo-red-japanese-maple?_pos=5&_sid=38ea8ef23&_ss=r", "https://mrmaple.com/products/buy-acer-palmatum-deshojo-red-japanese-maple?variant=43329754104035", "https://mrmaple.com/products/buy-acer-palmatum-deshojo-red-japanese-maple?variant=46006281109731"]
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
    print("Email sent!" if res.status_code == 200 else f"Email failed: {res.text}")

def run_check():
    print("Checking Shin Deshojo availability...")
    any_in_stock = False
    html_body = "<h3>Shin Deshojo In Stock!</h3><ul>"
    summary_lines = []

    for name, urls in PRODUCTS.items():
        try:
            if isinstance(urls, list):
                in_stock = False
                for url in urls:
                    if is_in_stock(url):
                        in_stock = True
                        html_body += f"<li><a href='{url}'>{name} is in stock</a></li>"
                        summary_lines.append(f"{name} is in stock at {url}")
                if not in_stock:
                    summary_lines.append(f"{name} is sold out")
            else:
                url = urls
                if is_in_stock(url):
                    any_in_stock = True
                    html_body += f"<li><a href='{url}'>{name} is in stock</a></li>"
                    summary_lines.append(f"{name} is in stock")
                else:
                    summary_lines.append(f"{name} is sold out")
        except Exception as e:
            summary_lines.append(f"Error checking {name}: {str(e)}")

    html_body += "</ul>"

    if any_in_stock:
        send_email("Shin Deshojo Available!", html_body)

    result = "\n".join(summary_lines)
    print(result)
    return result
