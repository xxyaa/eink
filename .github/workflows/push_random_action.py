
# scripts/push_random_action.py
import os
import random
import requests
import pandas as pd
import sys

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY") or os.environ.get("DOT_API_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
EXCEL_FILE = os.environ.get("EXCEL_FILE", "data.xlsx")

# 读取 Excel（无表头时，直接用列号）
df = pd.read_excel(EXCEL_FILE, header=None)

# 三列分别对应
titles = df.iloc[:, 0].dropna().tolist()      # 第1列 -> 标题
signatures = df.iloc[:, 1].dropna().tolist()  # 第2列 -> 签名
messages = df.iloc[:, 3].dropna().tolist()    # 第3列 -> 内容

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
    """随机推送一条"""
    idx = random.randint(0, len(messages) - 1)
    send_text(titles[idx], messages[idx], signatures[idx])

def auto_loop():
    """自动定时推送"""
    while True:
        push_random()
        time.sleep(SLEEP_TIME)

def manual_trigger():
    """等待用户手动回车推送"""
    while True:
        input("👉 按回车手动推送一条随机消息：")
        push_random()

# 启动两个线程：一个自动推送，一个手动触发
threading.Thread(target=auto_loop, daemon=True).start()
manual_trigger()  # 主线程监听键盘
