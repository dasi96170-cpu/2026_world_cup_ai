import time
import os
import sys
import requests
sys.stdout.reconfigure(encoding='utf-8')

from src.scraper import fetch_latest_news
from src.analyzer import analyze_news
from src.notifier import push_report

try:
    from config import TELEGRAM_BOT_TOKEN
except ImportError:
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def run_job():
    """供 GitHub Actions 雲端自動執行的一次性任務"""
    print("===== 開始執行世界盃情報自動抓取程序 =====")
    news_items = fetch_latest_news(limit=5)
    if not news_items:
        print("沒有抓到任何新聞，終止當次執行。")
        return
        
    report_text = analyze_news(news_items)
    print("\n[AI 報告預覽]\n" + report_text + "\n")
    push_report(report_text)
    
    print("正在將報告寫入靜態檔案 latest_report.md ...")
    with open("latest_report.md", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("===== 執行完畢 =====")

def send_message(chat_id, text):
    """回覆特定使用者的簡單封裝"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"發送回覆失敗: {e}")

def run_polling():
    """使用穩定的 requests 進行長輪詢 (Long Polling)，避開 Windows async 網路問題"""
    print("啟動輕量級互動機器人，正在監聽對話訊息... (按 Ctrl+C 結束)")
    offset = None
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    while True:
        try:
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
                
            response = requests.get(url, params=params, timeout=40)
            data = response.json()
            
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    text = message.get("text", "")
                    chat_id = message.get("chat", {}).get("id")
                    
                    if text == "/update":
                        send_message(chat_id, "🔍 收到指令！正在透過 Tavily AI 搜尋全球新聞並生成報告，請稍候約 10~20 秒...")
                        news_items = fetch_latest_news(limit=5)
                        if not news_items:
                            send_message(chat_id, "❌ 目前抓不到任何世界盃新聞，請稍後再試。")
                        else:
                            report_text = analyze_news(news_items)
                            send_message(chat_id, report_text)
                            
                    elif text == "/start":
                        send_message(chat_id, "⚽ 歡迎使用 2026 世界盃 AI 情報機器人！請輸入 /update 來獲取最新情報。")
                        
        except Exception as e:
            # 忽略 timeout 或連線不穩的錯誤，繼續輪詢
            time.sleep(3)

def main():
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run_job()
        print("☁️ GitHub Actions 雲端任務執行完畢，系統自動登出睡覺。")
        sys.exit(0)
        
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("⚠️ 未設定 TELEGRAM_BOT_TOKEN！無法啟動對話機器人。")
        sys.exit(1)
        
    run_polling()

if __name__ == "__main__":
    main()
