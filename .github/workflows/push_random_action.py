import os
import random
import requests
import pandas as pd
import time

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY") or os.environ.get("DOT_API_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
EXCEL_FILE = os.environ.get("EXCEL_FILE", "data.xlsx")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", "180"))  # 默认 3 分钟

# 读取 Excel
df = pd.read_excel(EXCEL_FILE, header=None)
titles = df.iloc[:, 0].dropna().tolist()
signatures = df.iloc[:, 1].dropna().tolist()
messages = df.iloc[:, 3].dropna().tolist()

def send_text(title, message, signature):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "refreshNow": True,
        "deviceId": DEVICE_ID,
        "title": title,
        "message": message,
        "signature": signature
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    print(f"[推送成功] 标题：{title}, 签名：{signature}, 内容：{message[:20]}...")
    print(response.json())

def push_random():
    idx = random.randint(0, len(messages) - 1)
    send_text(titles[idx], messages[idx], signatures[idx])

if __name__ == "__main__":
    while True:
        push_random()
        time.sleep(SLEEP_TIME)
