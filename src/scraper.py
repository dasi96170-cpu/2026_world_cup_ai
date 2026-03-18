import feedparser
import sys
import os

# 將專案根目錄加入路徑以便 import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RSS_FEEDS

def fetch_latest_news(limit=5):
    """從 RSS Feeds 抓取最新的足球新聞"""
    news_items = []
    
    for feed_url in RSS_FEEDS:
        print(f"Fetching from {feed_url}...")
        parsed_feed = feedparser.parse(feed_url)
        
        for entry in parsed_feed.entries[:limit]:
            title = entry.get('title', 'No Title')
            summary = entry.get('summary', 'No Summary')
            link = entry.get('link', '')
            
            news_items.append({
                "title": title,
                "summary": summary,
                "link": link
            })
            
            if len(news_items) >= limit:
                return news_items
                
    return news_items[:limit]

if __name__ == "__main__":
    news = fetch_latest_news(2)
    for n in news:
        print(n)
