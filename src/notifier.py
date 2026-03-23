import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID

def push_to_telegram(text):
    """發送訊息至 Telegram"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("your_"):
        print("⚠️ Telegram Token 尚未設定或無效，跳過 Telegram 發送。")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("🌟 Telegram 訊息已成功推播！")
        return True
    except Exception as e:
        print(f"Telegram 推播失敗: {str(e)}")
        return False

def push_to_line(text):
    """發送訊息至 LINE 官方帳號"""
    if not LINE_CHANNEL_ACCESS_TOKEN or LINE_CHANNEL_ACCESS_TOKEN.startswith("your_"):
        print("⚠️ LINE Channel Access Token 尚未設定或無效，跳過 LINE 發送。")
        return False
        
    if not LINE_USER_ID or LINE_USER_ID.startswith("your_"):
        print("⚠️ LINE User ID 尚未設定或無效，跳過 LINE 發送。")
        return False

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print("🌟 LINE 訊息已成功推播！")
        return True
    except Exception as e:
        print(f"LINE 推播失敗: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"詳細錯誤訊息: {e.response.text}")
        return False

def push_report(text):
    """統一發送報告介面：自動雙管齊下推播至有設定好的平台"""
    print("\n[開始進行跨平台推播]")
    tg_success = push_to_telegram(text)
    line_success = push_to_line(text)
    
    if not tg_success and not line_success:
        print("❌ 推播失敗：沒有任何平台設定成功，或網路皆無法連線。")
        return False
        
    print("[推播作業結束]\n")
    return True

if __name__ == "__main__":
    push_report("測試：這是一則來自 MVP 雙系統的廣播訊息！")
