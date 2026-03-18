import time
import schedule
import os
import sys
from src.scraper import fetch_latest_news
from src.analyzer import analyze_news
from src.notifier import push_report

def run_job():
    print("===== 開始執行世界盃情報自動抓取程序 =====")
    
    # 1. 抓取資料
    news_items = fetch_latest_news(limit=5)
    if not news_items:
        print("沒有抓到任何新聞，終止當次執行。")
        return
        
    # 2. 進行 LLM 分析（Gemini 會自動將翻譯好的標題與連結附在報告最後）
    report_text = analyze_news(news_items)
        
    # 3. 推播到 Telegram
    print("\n[AI 報告預覽]\n" + report_text + "\n")
    push_report(report_text)
    
    print("===== 執行完畢 =====")

if __name__ == "__main__":
    # 啟動時立刻執行一次
    run_job()
    
    # 若在雲端環境 (GitHub Actions) 執行，跑完一次就結束程式，不要進入無限迴圈
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print("☁️ GitHub Actions 雲端任務執行完畢，系統自動登出睡覺。")
        sys.exit(0)
    
    print("進入本機排程等待狀態... (每小時執行一次，按 Ctrl+C 中止)")
    schedule.every(1).hours.do(run_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
