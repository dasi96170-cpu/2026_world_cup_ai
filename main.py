import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

sys.stdout.reconfigure(encoding='utf-8')

from src.scraper import fetch_latest_news
from src.analyzer import analyze_news
from src.notifier import push_report

# 從專案設定或環境變數取得金鑰
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
    print("===== 執行完畢 =====")

# --- 互動式 Telegram Bot 指令 ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """使用者輸入 /start 時的打招呼訊息"""
    welcome_text = (
        "⚽ 歡迎使用 2026 世界盃 AI 情報樞紐機器人！\n\n"
        "目前我在這裡 24 小時待命，只要您輸入 /update ，"
        "我就會立刻爬取全球最新的戰況與分析報告給您喔！"
    )
    await update.message.reply_text(welcome_text)

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """使用者輸入 /update 時，立刻抓新聞並分析"""
    # 1. 先回覆收到指令，讓使用者知道我們有在做事
    await update.message.reply_text("🔍 收到指令！正在透過 Tavily AI 搜尋全球新聞並生成最新報告，請稍候約 10~20 秒...")
    
    # 2. 爬取與分析
    news_items = fetch_latest_news(limit=5)
    if not news_items:
        await update.message.reply_text("❌ 目前抓不到任何世界盃新聞，請稍後再試。")
        return
        
    report_text = analyze_news(news_items)
    
    # 3. 回傳完整的分析長文
    await update.message.reply_text(report_text)


def main():
    # 模式 A：若在雲端環境 (GitHub Actions) 執行，單次跑完就結束程式
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run_job()
        print("☁️ GitHub Actions 雲端任務執行完畢，系統自動登出睡覺。")
        sys.exit(0)
    
    # 模式 B：在本機執行互動式 Telegram 機器人 (監聽訊息)
    print("啟動互動式 Telegram 機器人，正在監聽對話訊息... (按 Ctrl+C 結束)")
    
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("⚠️ 未設定 TELEGRAM_BOT_TOKEN！無法啟動對話機器人。")
        sys.exit(1)
        
    # 建立應用程式
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # 註冊指令
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("update", update_command))
    
    # 開始輪詢 (Polling) 保持背景連線
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
