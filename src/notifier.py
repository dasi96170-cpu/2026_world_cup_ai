import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def push_report(text):
    """使用 requests 發送訊息，避開 Python 原生非同步函式庫的網路連線地雷"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("⚠️ Telegram Bot Token 尚未設定，無法發送通知。")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    
    try:
        # 直接打 API POST 請求
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # 若回傳 4xx 或 5xx 錯誤會自動拋出報錯
        print("🌟 Telegram 訊息已成功推播！請檢查手機！")
        return True
    except Exception as e:
        print(f"Telegram 推播失敗: {str(e)}")
        # 若是有更詳細的伺服器回傳錯誤也能印出
        if hasattr(e, 'response') and e.response is not None:
             print(f"詳細錯誤訊息: {e.response.text}")
        return False

if __name__ == "__main__":
    push_report("測試：這是一則來自 MVP 系統的訊息！")
