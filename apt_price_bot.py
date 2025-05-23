
import requests
import time
import csv
import os
import matplotlib.pyplot as plt
from telegram import Bot

# Konfigurasi
TELEGRAM_TOKEN = 'ISI_TOKEN_BOT_KAMU'
CHANNEL_ID = '@ISI_NAMA_CHANNEL_KAMU'
LOG_FILE = 'apt_price_log.csv'

bot = Bot(token=TELEGRAM_TOKEN)
last_price = None

def get_apt_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=aptos&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['aptos']['usd']

def save_to_log(price, timestamp):
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price])

def read_log():
    timestamps, prices = [], []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                timestamps.append(row[0])
                prices.append(float(row[1]))
    return timestamps, prices

def plot_price_history():
    timestamps, prices = read_log()
    if len(prices) < 5:
        return None
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices, marker='o', linestyle='-')
    plt.title('APT Price History')
    plt.xlabel('Waktu')
    plt.ylabel('Harga ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_file = 'price_chart.png'
    plt.savefig(image_file)
    plt.close()
    return image_file

while True:
    try:
        current_price = get_apt_price()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timestamp} - ${current_price}")

        if current_price != last_price:
            save_to_log(current_price, timestamp)
            bot.send_message(chat_id=CHANNEL_ID, text=f"{current_price}$")
            last_price = current_price

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as file:
                if sum(1 for _ in file) % 10 == 0:
                    chart = plot_price_history()
                    if chart:
                        bot.send_photo(chat_id=CHANNEL_ID, photo=open(chart, 'rb'))

        time.sleep(300)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
