from flask import Flask, request, jsonify, render_template
from crawl.crawl_api import get_product_reviews_api
from chatbot.summarizer import summarize_reviews, generate_product_review, answer_shopee_question, analyze_sentiments, preprocess_reviews, call_openai
from chatbot.plot import plot_sentiment_chart
import os
import random

app = Flask(__name__, static_folder="static", template_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

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
    # phân tích cảm xúc toàn bộ reviews
    all_sentiments = []
    filtered, _ = preprocess_reviews(reviews, max_reviews=60, max_chars=2000)
    for r in filtered:
        prompt = f"Phân tích cảm xúc của bình luận sau về sản phẩm Shopee và trả lời duy nhất 1 từ là 'positive', 'neutral' hoặc 'negative':\n{r}"
        messages = [
            {"role": "user", "content": prompt}
        ]
        sentiment = call_openai(messages)
        if not isinstance(sentiment, str):
            sentiment = "neutral"
        sentiment = sentiment.strip().lower()
        if "positive" in sentiment:
            sentiment = "positive"
        elif "negative" in sentiment:
            sentiment = "negative"
        elif "neutral" in sentiment:
            sentiment = "neutral"
        else:
            sentiment = "neutral"
        all_sentiments.append({"review": r, "sentiment": sentiment})
    # vẽ biểu đồ cho toàn bộ
    chart_path = plot_sentiment_chart(all_sentiments)
    # lấy 5 bình luận demo
    demo_reviews = random.sample(all_sentiments, min(5, len(all_sentiments)))
    # trả về kết quả
    return jsonify({
        "summary": summary,
        "file_path": crawl_result.get("file_path", None),
        "demo_reviews": demo_reviews,
        "chart_url": f"/static/{os.path.basename(chart_path)}"
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Hãy nhập nội dung"}), 400
    # nếu là link shopee thì xử lý như analyze
    if ("shopee.vn" in query and "/product/" in query) or "i." in query:
        crawl_result = get_product_reviews_api(query, format_type="xlsx")
        if not crawl_result or not crawl_result.get("success") or not crawl_result.get("data"):
            msg = crawl_result["message"] if crawl_result and "message" in crawl_result else "Không lấy được dữ liệu."
            return jsonify({"error": f"Không lấy được bình luận: {msg}"}), 500
        reviews = [item['comment'] for item in crawl_result['data'] if item and item.get('comment')]
        if not reviews:
            return jsonify({"error": "Không có bình luận hợp lệ"}), 500
        summary = summarize_reviews(reviews)
        # Phân tích cảm xúc toàn bộ reviews để vẽ biểu đồ
        all_sentiments = []
        filtered, _ = preprocess_reviews(reviews, max_reviews=60, max_chars=2000)
        for r in filtered:
            prompt = f"Phân tích cảm xúc của bình luận sau về sản phẩm Shopee và trả lời duy nhất 1 từ là 'positive', 'neutral' hoặc 'negative':\n{r}"
            messages = [
                {"role": "user", "content": prompt}
            ]
            sentiment = call_openai(messages)
            if not isinstance(sentiment, str):
                sentiment = "neutral"
            sentiment = sentiment.strip().lower()
            if "positive" in sentiment:
                sentiment = "positive"
            elif "negative" in sentiment:
                sentiment = "negative"
            elif "neutral" in sentiment:
                sentiment = "neutral"
            else:
                sentiment = "neutral"
            all_sentiments.append({"review": r, "sentiment": sentiment})
        chart_path = plot_sentiment_chart(all_sentiments)
        # Lấy 5 bình luận demo từ toàn bộ
        demo_reviews = random.sample(all_sentiments, min(5, len(all_sentiments)))
        review_text = generate_product_review(reviews, all_sentiments)
        if not review_text or review_text.strip() == "":
            review_text = "Không thể tạo nhận xét sản phẩm vào lúc này."
        return jsonify({
            "summary": summary,
            "file_path": crawl_result.get("file_path", None),
            "demo_reviews": demo_reviews,
            "chart_url": f"/static/{os.path.basename(chart_path)}",
            "product_review": review_text
        })
    # nếu là câu hỏi về nền tảng thì dùng mô hình sinh văn bản tiếng Việt để trả lời
    answer = answer_shopee_question(query)
    if not answer or answer.strip() == "":
        answer = "Không thể trả lời câu hỏi vào lúc này"
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
