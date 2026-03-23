from flask import Flask, render_template, jsonify
import os
import traceback
from src.scraper import fetch_latest_news
from src.analyzer import analyze_news
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    """渲染首頁 Dashboard"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['GET'])
def analyze():
    """提供前端 Ajax 呼叫的 API，抓取新聞並作 AI 分析"""
    try:
        # 抓取最新的世界盃相關新聞
        news_items = fetch_latest_news(limit=5)
        
        if not news_items:
            return jsonify({
                "status": "error",
                "message": "目前抓不到任何世界盃新聞，請稍後再試。"
            }), 404
            
        # 呼叫 Gemini 分析
        report_text = analyze_news(news_items)
        
        return jsonify({
            "status": "success",
            "report": report_text,
            "news_count": len(news_items)
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"分析過程發生錯誤：{str(e)}"
        }), 500

if __name__ == '__main__':
    # 開啟 Debug 模式，方便開發時熱更新
    app.run(host='0.0.0.0', port=5000, debug=True)
