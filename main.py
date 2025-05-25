from flask import Flask, request, jsonify, render_template, send_from_directory
from crawl.crawl_api import get_product_reviews_api
from chatbot.summarizer import summarize_reviews, generate_product_review, answer_shopee_question, analyze_sentiments, preprocess_reviews, call_openai
from chatbot.plot import plot_sentiment_chart
import os
import random

# Đường dẫn tuyệt đối tới thư mục build
BUILD_PATH = os.path.join('D:/NCKH/shopee-review-analyzer/shopee-sentiment/build')
CHARTS_DIR = os.path.join('D:/NCKH/shopee-review-analyzer/charts')

app = Flask(__name__, static_folder=os.path.join(BUILD_PATH, 'static'))

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

if __name__ == "__main__":
    app.run(debug=True)