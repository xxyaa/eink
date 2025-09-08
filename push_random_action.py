import os
import random
import requests
import pandas as pd
from datetime import datetime

# ================= 配置 =================
API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY") or os.environ.get("DOT_API_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
EXCEL_FILE = os.environ.get("EXCEL_FILE", "data.xlsx")
# =======================================

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
        "refreshNow": False,
        "deviceId": DEVICE_ID,
        "title": title,
        "message": message,
        "signature": signature
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print("=== 推送详情 ===")
        print("时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("标题：", title)
        print("签名：", signature)
        print("内容：", message[:80])
        print("API 返回：", response.json())
        print("================\n")
    except Exception as e:
        print(f"发送失败：{e}")

def push_random():
    idx = random.randint(0, len(messages) - 1)
    send_text(titles[idx], messages[idx], signatures[idx])

if __name__ == "__main__":
    push_random()
