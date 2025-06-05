from flask import Flask, request, jsonify, render_template, send_from_directory, session
from crawl.crawl_api import get_product_reviews_api
from chatbot.summarizer import (
    summarize_reviews, generate_product_review, answer_shopee_question, 
    analyze_sentiments, preprocess_reviews, call_openai,
    analyze_review_keywords, highlight_reviews_by_sentiment,
    extract_product_features, get_sentiment_keywords,
    get_crawled_data_info, get_demo_reviews_with_highlights, 
    generate_overall_assessment
)
from chatbot.plot import plot_sentiment_chart
from flask_cors import CORS
from pymongo import MongoClient
from datetime import timedelta
from models.user import User
from models.chat_history import ChatHistory
from datetime import datetime
from config import Config 
from utils.security import (
    hash_password, 
    verify_password, 
    create_access_token,
    decode_token
)
from dotenv import load_dotenv
import os
import random

# Lấy đường dẫn thư mục hiện tại (nơi app.py đang chạy)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn tương đối tới các thư mục
BUILD_PATH = os.path.join(BASE_DIR, 'shopee-sentiment', 'build')
CHARTS_DIR = os.path.join(BASE_DIR, 'charts')

load_dotenv()

app = Flask(__name__, 
           static_folder=os.path.join(BUILD_PATH, 'static'),
           static_url_path='/static')

# Thêm secret key cho session
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')

CORS(app)  # Thêm CORS để tránh lỗi cross-origin

# Tạo thư mục charts nếu chưa tồn tại
os.makedirs(CHARTS_DIR, exist_ok=True)

# Route frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(BUILD_PATH, path)):
        return send_from_directory(BUILD_PATH, path)
    else:
        return send_from_directory(BUILD_PATH, 'index.html')

# Route để phục vụ biểu đồ từ thư mục charts
@app.route('/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(CHARTS_DIR, filename)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "không có url được cung cấp"}), 400
    
    print(f"DEBUG: Analyzing URL: {url}")
    
    # crawl
    crawl_result = get_product_reviews_api(url, format_type="xlsx")
    if not crawl_result or not crawl_result.get("success"):
        msg = crawl_result.get("message", "Không lấy được dữ liệu.") if crawl_result else "Không lấy được dữ liệu."
        return jsonify({"error": f"Không lấy được bình luận: {msg}"}), 500
    
    # Kiểm tra data có tồn tại không
    if not crawl_result.get("data"):
        return jsonify({"error": "Không có dữ liệu bình luận"}), 500
    
    reviews = [item['comment'] for item in crawl_result['data'] if item and item.get('comment')]
    if not reviews:
        return jsonify({"error": "Không có bình luận hợp lệ"}), 500
    
    print(f"DEBUG: Found {len(reviews)} reviews")
    
    # show thông tin dữ liệu đã crawl (Section 1)
    crawled_data_info = get_crawled_data_info(reviews)
    print(f"DEBUG: crawled_data_info = {crawled_data_info}")
    
    # Tóm tắt với highlights
    summary = summarize_reviews(reviews)
      # Phân tích từ khóa
    highlighted_reviews, keywords = analyze_review_keywords(reviews)
    product_features = extract_product_features(reviews)
    
    # Phân tích cảm xúc - sử dụng tất cả dữ liệu cho biểu đồ/thống kê
    all_sentiments = []
    filtered, _ = preprocess_reviews(reviews, max_reviews=len(reviews), max_chars=10000)
    for r in filtered:
        prompt = f"Phân tích cảm xúc của bình luận sau về sản phẩm Shopee và trả lời duy nhất 1 từ là 'positive', 'neutral' hoặc 'negative':\n{r}"
        messages = [{"role": "user", "content": prompt}]
        sentiment = call_openai(messages)
        
        if not isinstance(sentiment, str):
            sentiment = "neutral"
        sentiment = sentiment.strip().lower()
        
        if "positive" in sentiment:
            sentiment = "positive"
        elif "negative" in sentiment:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        all_sentiments.append({"review": r, "sentiment": sentiment})
    
    # Demo 5 positive + 5 negative reviews với highlights (Section 2)
    demo_reviews_with_highlights = get_demo_reviews_with_highlights(all_sentiments)
    
    # Highlight reviews theo cảm xúc (cho backward compatibility)
    highlighted_sentiment_reviews = highlight_reviews_by_sentiment(all_sentiments)
    sentiment_keywords = get_sentiment_keywords(all_sentiments)
    
    # Lấy 5 positive và 5 negative reviews thay vì random (legacy)
    positive_reviews = [r for r in highlighted_sentiment_reviews if r["sentiment"] == "positive"]
    negative_reviews = [r for r in highlighted_sentiment_reviews if r["sentiment"] == "negative"]
    
    demo_reviews = {
        "positive": positive_reviews[:5],
        "negative": negative_reviews[:5]
    }
    
    # Đánh giá tổng thể cuối cùng (Section 3)
    overall_assessment = generate_overall_assessment(reviews, all_sentiments, summary, keywords)
    
    # Vẽ biểu đồ
    chart_path = plot_sentiment_chart(all_sentiments)
    
    # Trích xuất tên sản phẩm
    product_name = extract_product_name(url)
    
    # Trích xuất hình ảnh sản phẩm
    product_image = extract_product_image(url)
      # Gợi ý sản phẩm liên quan
    related_products = suggest_related_products(product_name, keywords)
    
    print(f"DEBUG: Before returning JSON - demo_reviews_with_highlights: {type(demo_reviews_with_highlights)}")
    print(f"DEBUG: Before returning JSON - overall_assessment: {type(overall_assessment)}")
    
    return jsonify({
        "summary": summary,
        "file_path": crawl_result.get("file_path", None),
        
        # Legacy demo reviews (for backward compatibility)
        "demo_reviews": demo_reviews,
        
        "crawled_data_info": crawled_data_info,
        "demo_reviews_with_highlights": demo_reviews_with_highlights,
        "overall_assessment": overall_assessment,
        
        "chart_url": f"/charts/{os.path.basename(chart_path)}",
        "keywords": keywords,
        "sentiment_keywords": sentiment_keywords,
        "product_features": product_features,
        "product_name": product_name,
        "product_image": product_image,
        "related_products": related_products,
        "suggested_questions": generate_suggested_questions(summary)
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Hãy nhập nội dung"}), 400
    
    # Lấy chat history từ session
    chat_history = session.get('chat_history', [])
    
    if ("shopee.vn" in query and "/product/" in query) or "i." in query:
        # Xử lý tương tự như analyze
        crawl_result = get_product_reviews_api(query, format_type="xlsx")
        if not crawl_result or not crawl_result.get("success") or not crawl_result.get("data"):
            msg = crawl_result["message"] if crawl_result and "message" in crawl_result else "Không lấy được dữ liệu."
            return jsonify({"error": f"Không lấy được bình luận: {msg}"}), 500
        reviews = [item['comment'] for item in crawl_result['data'] if item and item.get('comment')]
        if not reviews:
            return jsonify({"error": "Không có bình luận hợp lệ"}), 500
        
        # Hiển thị thông tin dữ liệu đã crawl (Section 1)
        crawled_data_info = get_crawled_data_info(reviews)
          # Tóm tắt với highlights
        summary = summarize_reviews(reviews)
        
        # Phân tích từ khóa
        highlighted_reviews, keywords = analyze_review_keywords(reviews)
        product_features = extract_product_features(reviews)
        # Phân tích cảm xúc
        all_sentiments = []
        filtered, _ = preprocess_reviews(reviews, max_reviews=len(reviews), max_chars=20000)
        for r in filtered:
            prompt = f"Phân tích cảm xúc của bình luận sau về sản phẩm Shopee và trả lời duy nhất 1 từ là 'positive', 'neutral' hoặc 'negative':\n{r}"
            messages = [{"role": "user", "content": prompt}]
            sentiment = call_openai(messages)
            
            if not isinstance(sentiment, str):
                sentiment = "neutral"
            sentiment = sentiment.strip().lower()
            
            if "positive" in sentiment:
                sentiment = "positive"
            elif "negative" in sentiment:
                sentiment = "negative"
            else:
                sentiment = "neutral"
                
            all_sentiments.append({"review": r, "sentiment": sentiment})
        
        # Demo 5 positive + 5 negative reviews với highlights (Section 2)
        demo_reviews_with_highlights = get_demo_reviews_with_highlights(all_sentiments)
        
        # Highlight reviews theo cảm xúc (cho backward compatibility)
        highlighted_sentiment_reviews = highlight_reviews_by_sentiment(all_sentiments)
        sentiment_keywords = get_sentiment_keywords(all_sentiments)
        
        # Lấy 5 positive và 5 negative reviews thay vì random (legacy)
        positive_reviews = [r for r in highlighted_sentiment_reviews if r["sentiment"] == "positive"]
        negative_reviews = [r for r in highlighted_sentiment_reviews if r["sentiment"] == "negative"]
        
        demo_reviews = {
            "positive": positive_reviews[:5],
            "negative": negative_reviews[:5]
        }
        
        # Đánh giá tổng thể cuối cùng (Section 3)
        overall_assessment = generate_overall_assessment(reviews, all_sentiments, summary, keywords)
        
        # Vẽ biểu đồ 
        chart_path = plot_sentiment_chart(all_sentiments)
        
        # Trích xuất tên sản phẩm từ URL hoặc HTML
        product_name = extract_product_name(query)
        
        # Trích xuất hình ảnh sản phẩm
        product_image = extract_product_image(query)
        
        # Gợi ý sản phẩm liên quan
        related_products = suggest_related_products(product_name, keywords)
        
        # Lưu vào chat history
        chat_history.append({
            "query": query,
            "response": "Phân tích sản phẩm thành công",
            "timestamp": datetime.now().isoformat()
        })
        session['chat_history'] = chat_history[-20:]  # Giữ 20 tin nhắn gần nhất
        return jsonify({
            "summary": summary,
            "file_path": crawl_result.get("file_path", None),
            
            # Legacy demo reviews (for backward compatibility)
            "demo_reviews": demo_reviews,
            
            # New sections
            "crawled_data_info": crawled_data_info,
            "demo_reviews_with_highlights": demo_reviews_with_highlights,
            "overall_assessment": overall_assessment,
            
            "chart_url": f"/charts/{os.path.basename(chart_path)}",
            "keywords": keywords,
            "sentiment_keywords": sentiment_keywords,
            "product_features": product_features,
            "product_name": product_name,
            "product_image": product_image,
            "related_products": related_products,
            "suggested_questions": generate_suggested_questions(summary)
        })
    
    else:
        # Xử lý câu hỏi thông thường với context
        answer = answer_shopee_question(query, chat_history)
        
        # Lưu vào chat history
        chat_history.append({
            "query": query,
            "response": answer,
            "timestamp": datetime.now().isoformat()
        })
        session['chat_history'] = chat_history[-20:]
        
        return jsonify({
            "answer": answer,
            "suggested_questions": generate_suggested_questions(answer)
        })

def extract_product_name(url_or_query):
    """Trích xuất tên sản phẩm từ URL Shopee"""
    try:
        if "shopee.vn" in url_or_query:
            import urllib.parse
            import re
            
            # Làm sạch URL trước
            url_or_query = url_or_query.split('?')[0]  # Loại bỏ query parameters
            
            # Trích xuất tên từ URL trực tiếp
            # URL format: https://shopee.vn/Ten-San-Pham-i.123.456
            if "/product/" in url_or_query:
                # Format mới: /product/123/456?sp=...
                parts = url_or_query.split("/product/")[0]
                if "/" in parts:
                    product_name = parts.split("/")[-1]
                else:
                    product_name = "Sản phẩm Shopee"
            else:
                # Format phổ biến: /Ten-San-Pham-i.123.456
                parts = url_or_query.split("/")
                product_name = "Sản phẩm Shopee"
                
                for part in reversed(parts):
                    if part and "-i." in part:
                        # Lấy phần tên trước "-i."
                        product_name = part.split("-i.")[0]
                        break
                    elif part and "i." in part and "." in part.split("i.")[1]:
                        # Format: Ten-San-Pham-i.123.456
                        product_name = part.split("-i.")[0] if "-i." in part else part
                        break
                    elif part and not part.startswith("i.") and len(part) > 5 and not part.isdigit():
                        # Tên sản phẩm thông thường
                        product_name = part
                        break
            
            # Decode URL và làm sạch tên
            product_name = urllib.parse.unquote(product_name)
            
            # Làm sạch tên sản phẩm
            product_name = product_name.replace("-", " ").replace("_", " ")
            product_name = re.sub(r'[^\w\s\u00C0-\u1EF9]', ' ', product_name)  # Giữ tiếng Việt
            product_name = re.sub(r'\s+', ' ', product_name).strip()  # Loại bỏ khoảng trắng thừa
            
            # Capitalize từng từ
            words = product_name.split()
            product_name = " ".join(word.capitalize() for word in words if len(word) > 1)
            
            return product_name if len(product_name) > 3 else "Sản phẩm Shopee"
        
        return "Sản phẩm Shopee"
    except Exception as e:
        print(f"Error extracting product name: {e}")
        return "Sản phẩm Shopee"

def extract_product_image(url_or_query):
    """Trích xuất hình ảnh sản phẩm từ URL Shopee"""
    try:
        if "shopee.vn" in url_or_query:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url_or_query, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Tìm hình ảnh sản phẩm
                img_selectors = [
                    'img[class*="product"]',
                    'img[class*="main"]', 
                    '.product-image img',
                    '.image-container img',
                    'meta[property="og:image"]'
                ]
                
                for selector in img_selectors:
                    if selector.startswith('meta'):
                        meta_tag = soup.find('meta', {'property': 'og:image'})
                        if meta_tag and meta_tag.get('content'):
                            return meta_tag.get('content')
                    else:
                        img_tag = soup.select_one(selector)
                        if img_tag and img_tag.get('src'):
                            img_url = img_tag.get('src')
                            if img_url.startswith('//'):
                                img_url = 'https:' + img_url
                            elif img_url.startswith('/'):
                                img_url = 'https://shopee.vn' + img_url
                            return img_url
        return None
    except Exception as e:
        print(f"Error extracting product image: {e}")
        return None

def suggest_related_products(product_name, keywords):
    """Gợi ý sản phẩm liên quan dựa trên tên sản phẩm và từ khóa"""
    # Tạo gợi ý dựa trên từ khóa
    if not keywords:
        return []
    
    # Lấy từ khóa chính
    main_keywords = [kw[0] for kw in keywords[:5]]
    
    suggestions = []
    base_searches = [
        f"{product_name} tương tự",
        f"{product_name} cùng loại",
        f"{product_name} giá rẻ",
        f"{product_name} chất lượng cao"
    ]
    
    # Thêm gợi ý dựa trên từ khóa
    for keyword in main_keywords:
        suggestions.append(f"Sản phẩm {keyword}")
        suggestions.append(f"{keyword} tốt nhất")
    
    suggestions.extend(base_searches)
    return suggestions[:8]  # Trả về 8 gợi ý

def generate_suggested_questions(context):
    """Tạo câu hỏi gợi ý dựa trên context"""
    suggestions = [
        "Sản phẩm này có chất lượng như thế nào?",
        "Giá cả có phù hợp không?",
        "Có nên mua sản phẩm này không?",
        "Những ưu điểm nổi bật của sản phẩm?",
        "Những nhược điểm cần lưu ý?"
    ]
    return suggestions[:3]  # Trả về 3 câu hỏi gợi ý

if __name__ == "__main__":
    app.run(debug=True, port=5000)