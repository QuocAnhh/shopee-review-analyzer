from flask import Flask, request, jsonify, render_template, send_from_directory
from crawl.crawl_api import get_product_reviews_api
from chatbot.summarizer import summarize_reviews, generate_product_review, answer_shopee_question, analyze_sentiments, preprocess_reviews, call_openai
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
BUILD_PATH = os.path.normpath(os.path.join(BASE_DIR, '..','shopee-review-analyzer', 'shopee-sentiment', 'build'))
CHARTS_DIR = os.path.join(BASE_DIR,'shopee-review-analyzer', 'charts')

# Kiểm tra đường dẫn
print(f"Build path: {BUILD_PATH}")
print(f"Build exists: {os.path.exists(BUILD_PATH)}")
print(f"Index.html exists: {os.path.exists(os.path.join(BUILD_PATH, 'index.html'))}")

load_dotenv()

app = Flask(__name__, 
           static_folder=os.path.join(BUILD_PATH, 'static'),
           static_url_path='/static')

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
    
    # crawl
    crawl_result = get_product_reviews_api(url, format_type="xlsx")
    if not crawl_result or not crawl_result.get("success") or not crawl_result.get("data"):
        msg = crawl_result["message"] if crawl_result and "message" in crawl_result else "Không lấy được dữ liệu."
        return jsonify({"error": f"Không lấy được bình luận: {msg}"}), 500
    
    reviews = [item['comment'] for item in crawl_result['data'] if item and item.get('comment')]
    if not reviews:
        return jsonify({"error": "Không có bình luận hợp lệ"}), 500
    
    # tóm tắt
    summary = summarize_reviews(reviews)
    
    # phân tích cảm xúc
    all_sentiments = []
    filtered, _ = preprocess_reviews(reviews, max_reviews=60, max_chars=2000)
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
    
    # vẽ biểu đồ
    chart_path = plot_sentiment_chart(all_sentiments)
    
    # lấy 5 bình luận demo
    demo_reviews = random.sample(all_sentiments, min(5, len(all_sentiments)))
    
    return jsonify({
        "summary": summary,
        "file_path": crawl_result.get("file_path", None),
        "demo_reviews": demo_reviews,
        "chart_url": f"/charts/{os.path.basename(chart_path)}"
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Hãy nhập nội dung"}), 400
    
    if ("shopee.vn" in query and "/product/" in query) or "i." in query:
        # Xử lý tương tự như analyze
        crawl_result = get_product_reviews_api(query, format_type="xlsx")
        if not crawl_result or not crawl_result.get("success") or not crawl_result.get("data"):
            msg = crawl_result["message"] if crawl_result and "message" in crawl_result else "Không lấy được dữ liệu."
            return jsonify({"error": f"Không lấy được bình luận: {msg}"}), 500
        
        reviews = [item['comment'] for item in crawl_result['data'] if item and item.get('comment')]
        if not reviews:
            return jsonify({"error": "Không có bình luận hợp lệ"}), 500
        
        summary = summarize_reviews(reviews)
        all_sentiments = []
        filtered, _ = preprocess_reviews(reviews, max_reviews=60, max_chars=2000)
        
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
        
        chart_path = plot_sentiment_chart(all_sentiments)
        demo_reviews = random.sample(all_sentiments, min(5, len(all_sentiments)))
        review_text = generate_product_review(reviews, all_sentiments)
        
        if not review_text or review_text.strip() == "":
            review_text = "Không thể tạo nhận xét sản phẩm vào lúc này."
        
        return jsonify({
            "summary": summary,
            "file_path": crawl_result.get("file_path", None),
            "demo_reviews": demo_reviews,
            "chart_url": f"/charts/{os.path.basename(chart_path)}",
            "product_review": review_text
        })
    
    # Xử lý câu hỏi thông thường
    answer = answer_shopee_question(query)
    if not answer or answer.strip() == "":
        answer = "Không thể trả lời câu hỏi vào lúc này"
    
    return jsonify({"answer": answer})

client = MongoClient(Config.MONGO_URI)
db = client.get_database()
user_model = User(db)
chat_history_model = ChatHistory(db)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'confirmPassword']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    if data['password'] != data['confirmPassword']:
        return jsonify({"error": "Passwords do not match"}), 400
    
    # Check if user already exists
    if user_model.find_user_by_email(data['email']):
        return jsonify({"error": "Email already registered"}), 409
    
    # Hash password and create user
    hashed_password = hash_password(data['password'])
    user_id = user_model.create_user(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_password
    )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400
    
    user = user_model.find_user_by_email(data['email'])
    if not user or not verify_password(data['password'], user['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user['_id'])},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email']
        }
    })

@app.route('/api/me', methods=['GET'])
def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = decode_token(token)
        user_id = payload.get('sub')
        if not user_id:
            return jsonify({"error": "Invalid token"}), 401
        
        user = user_model.find_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email']
        })
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route('/api/history', methods=['GET'])
def get_history():
    user_id = get_current_user_id()  # Implement your auth logic
    history = chat_history_model.get_user_history(user_id)
    return jsonify([{
        "id": str(item["_id"]),
        "title": item["title"],
        "preview": get_preview(item["messages"]),
        "time": format_time(item["updated_at"])
    } for item in history])

@app.route('/api/history/<history_id>', methods=['GET'])
def get_history_detail(history_id):
    user_id = get_current_user_id()
    history = chat_history_model.get_history_by_id(history_id, user_id)
    if not history:
        return jsonify({"error": "History not found"}), 404
    return jsonify({
        "id": str(history["_id"]),
        "title": history["title"],
        "messages": history["messages"],
        "time": format_time(history["updated_at"])
    })

@app.route('/api/history/<history_id>', methods=['DELETE'])
def delete_history(history_id):
    user_id = get_current_user_id()
    if chat_history_model.delete_history(history_id, user_id):
        return jsonify({"message": "Deleted successfully"})
    return jsonify({"error": "History not found"}), 404

@app.route('/api/history', methods=['POST'])
def save_history():
    user_id = get_current_user_id()
    data = request.json
    history_id = chat_history_model.create_history(
        user_id=user_id,
        title=data["title"],
        messages=data["messages"]
    )
    return jsonify({"id": history_id}), 201

# Helper functions
def get_current_user_id():
    # Implement your authentication logic
    # Example: get from JWT token
    return "user123"  # Replace with actual user ID from auth

def get_preview(messages):
    # Get last user message as preview
    for msg in reversed(messages):
        if msg.get("isUser"):
            return msg["content"]
    return "No messages"

def format_time(timestamp):
    now = datetime.utcnow()
    delta = now - timestamp
    if delta.days > 7:
        return timestamp.strftime("%d/%m/%Y")
    elif delta.days > 0:
        return f"{delta.days} ngày trước"
    elif delta.seconds > 3600:
        return f"{delta.seconds // 3600} giờ trước"
    else:
        return f"{delta.seconds // 60} phút trước"

if __name__ == "__main__":
    app.run(debug=True, port=5000)