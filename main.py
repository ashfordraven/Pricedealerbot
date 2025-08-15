# Pricedealerbot - Zero-cost Amazon & Flipkart Deal Alert Bot
# Free hosting compatible (Replit, Railway, Render)
# Telegram Bot Token: 7982458977:AAFCf7N1Mt5nxCHL8d0OnBrrAecPAXfMZjk

import requests
from bs4 import BeautifulSoup
import json
import time

# --------- CONFIG ---------
TELEGRAM_TOKEN = "7982458977:AAFCf7N1Mt5nxCHL8d0OnBrrAecPAXfMZjk"
TELEGRAM_CHAT_ID = "@Pricedealer"
CHECK_INTERVAL = 900  # seconds (15 minutes)
DEALS_FILE = "sent_deals.json"
MIN_DISCOUNT_PERCENT = 90
# ---------------------------

# Load sent deals to avoid duplicates
try:
    with open(DEALS_FILE, "r") as f:
        sent_deals = json.load(f)
except:
    sent_deals = []

# Utility function: send Telegram alert
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram send failed:", e)

# Utility function: parse Amazon page
def check_amazon_deals(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        title_tag = soup.find(id="productTitle")
        price_tag = soup.find("span", {"class": "a-price-whole"})
        original_tag = soup.find("span", {"class": "priceBlockStrikePriceString"})
        
        if not title_tag or not price_tag:
            return None
        
        title = title_tag.get_text().strip()
        current_price = int(price_tag.get_text().replace(",", "").strip())
        original_price = int(original_tag.get_text().replace("₹", "").replace(",", "").strip()) if original_tag else current_price
        discount = int((original_price - current_price) / original_price * 100)
        
        if discount >= MIN_DISCOUNT_PERCENT and url not in sent_deals:
            sent_deals.append(url)
            with open(DEALS_FILE, "w") as f:
                json.dump(sent_deals, f)
            
            message = f"🔥 Deal Alert! 🔥\nProduct: {title}\nCurrent Price: ₹{current_price}\nOriginal Price: ₹{original_price}\nDiscount: {discount}%\nBuy Now: {url}"
            send_telegram(message)
    except Exception as e:
        print("Amazon check failed:", e)

# Utility function: parse Flipkart page
def check_flipkart_deals(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        title_tag = soup.find("span", {"class": "B_NuCI"})
        current_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        original_tag = soup.find("div", {"class": "_3I9_wc _2p6lqe"})
        
        if not title_tag or not current_tag:
            return None
        
        title = title_tag.get_text().strip()
        current_price = int(current_tag.get_text().replace("₹", "").replace(",", "").strip())
        original_price = int(original_tag.get_text().replace("₹", "").replace(",", "").strip()) if original_tag else current_price
        discount = int((original_price - current_price) / original_price * 100)
        
        if discount >= MIN_DISCOUNT_PERCENT and url not in sent_deals:
            sent_deals.append(url)
            with open(DEALS_FILE, "w") as f:
                json.dump(sent_deals, f)
            
            message = f"🔥 Deal Alert! 🔥\nProduct: {title}\nCurrent Price: ₹{current_price}\nOriginal Price: ₹{original_price}\nDiscount: {discount}%\nBuy Now: {url}"
            send_telegram(message)
    except Exception as e:
        print("Flipkart check failed:", e)

# --- MAIN LOOP ---
def main():
    # Add Amazon/Flipkart product URLs to monitor
    amazon_urls = [
        "https://www.amazon.in/dp/B09XYZ...",  # replace with actual product links
    ]
    flipkart_urls = [
        "https://www.flipkart.com/item?p=XYZ...",  # replace with actual product links
    ]
    
    while True:
        for url in amazon_urls:
            check_amazon_deals(url)
        for url in flipkart_urls:
            check_flipkart_deals(url)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()


