import os
import sys

# 若是在命令列直接測試，需要載入 .env
# 但若從 main.py or app.py 呼叫，.env 已在他的最外層被載入。
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from tavily import TavilyClient
except ImportError:
    print("尚未安裝 tavily-python！請執行 pip install tavily-python")
    TavilyClient = None

def fetch_latest_news(limit=5):
    """使用 Tavily AI 搜尋最新 2026 世界盃情報"""
    news_items = []
    
    api_key = os.environ.get("TAVILY_API_KEY")
    print(f"Debug: api_key={api_key[:5] if api_key else None}, TavilyClient installed={TavilyClient is not None}", flush=True)
    if not api_key or not TavilyClient:
        print("錯誤：缺少 TAVILY_API_KEY 或 tavily 套件。")
        return []
        
    client = TavilyClient(api_key=api_key)
    
    print("Using Tavily AI Search to fetch world cup news...", flush=True)
    response = client.search(
        query="2026 FIFA World Cup soccer latest news",
        search_depth="advanced",
        max_results=limit
    )
    
    for result in response.get("results", []):
        news_items.append({
            "title": result.get("title", "No Title"),
            "summary": result.get("content", "No Content"),
            "link": result.get("url", "")
        })
        
    return news_items

if __name__ == "__main__":
    news = fetch_latest_news(2)
    for i, n in enumerate(news, 1):
        print(f"[{i}] {n['title']}\n{n['summary']}\n{n['link']}\n")
