import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("8270420875:AAHJ1jaJB360Wo8QwbQBLRfmvGrdAGIjsEM")
CHAT_ID = os.getenv("6965622706")

LAST_PRICE = ""

URL = "https://www.keralagold.com/daily-gold-prices.htm"

def get_latest_pavan_price():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            text = cols[1].text.strip()
            if "Rs." in text:
                return text
    return None

def send_telegram(message):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": message
    })

while True:
    try:
        price = get_latest_pavan_price()

        if price and price != LAST_PRICE:
            LAST_PRICE = price
            send_telegram(
                "🔔 Kerala Gold Rate Update\n\n"
                f"22K Gold (8g / Pavan): {price}\n\n"
                "Source: keralagold.com"
            )

        time.sleep(600)  # check every 10 minutes

    except:
        time.sleep(600)
