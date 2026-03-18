import os
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 世界盃 / 體育新聞 RSS 來源 (可後續動態擴充)
RSS_FEEDS = [
    "https://www.espn.com/espn/rss/soccer/news",
    "http://feeds.bbci.co.uk/sport/football/rss.xml"
]
