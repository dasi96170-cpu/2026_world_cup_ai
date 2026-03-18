from google import genai
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY

def analyze_news(news_items):
    """使用 Gemini API 來分析新聞，包含重點與情緒分析"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return "⚠️ API Key 尚未設定，無法進行 AI 分析。\n請在 .env 檔案中設定 GEMINI_API_KEY。"
        
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    content_to_analyze = "以下是今日最新的幾則世界盃相關足球新聞：\n\n"
    for i, item in enumerate(news_items, 1):
        content_to_analyze += f"({i}) 標題：{item['title']}\n摘要：{item['summary']}\n網址：{item['link']}\n\n"
        
    prompt = (
        content_to_analyze +
        "請根據以上新聞：\n"
        "1. 用繁體中文總結出「今日 3 大重點洞察」。\n"
        "2. 給出整體的新聞情緒評估（例如：正面、中立、負面或有爭議），簡單說明理由。\n"
        "3. 在報告的最後，請加上「🔗 新聞來源連結：」區塊，將上述所有新聞來源列出，格式必須為：\n📌 英文原始標題 (繁體中文翻譯標題)\n原始網址連結\n\n"
        "請使用「純文字」格式輸出排版，【絕對不要】使用任何 Markdown 符號（如 ** 或 * 或 #），以免後續通訊軟體推播失敗。"
    )
    
    print("Calling Gemini API...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI 分析發生錯誤: {str(e)}"

if __name__ == "__main__":
    mock_news = [{"title": "Test Title", "summary": "Test Summary", "link": ""}]
    print(analyze_news(mock_news))
