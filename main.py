from flask import Flask, request, jsonify, render_template
from crawl.crawl_api import get_product_reviews_api
from chatbot.summarizer import summarize_reviews, generate_product_review, answer_shopee_question, analyze_sentiments
from chatbot.plot import plot_sentiment_chart
import os

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
    crawl_result = get_product_reviews_api(url, format_type="json")
    if not crawl_result["success"] or not crawl_result["data"]:
        return jsonify({"error": f"Không lấy được bình luận: {crawl_result['message']}"}), 500
    reviews = [item['comment'] for item in crawl_result['data'] if item.get('comment')]
    if not reviews:
        return jsonify({"error": "Không có bình luận hợp lệ"}), 500
    # tóm tắt
    summary = summarize_reviews(reviews)
    # phân tích cảm xúc (dùng hàm mới từ summarizer.py)
    sentiments = analyze_sentiments(reviews)
    # vẽ biểu đồ
    chart_path = plot_sentiment_chart(sentiments)
    # trả về kết quả
    return jsonify({
        "summary": summary,
        "sentiments": sentiments,
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
        crawl_result = get_product_reviews_api(query, format_type="json")
        if not crawl_result["success"] or not crawl_result["data"]:
            return jsonify({"error": f"Không lấy được bình luận: {crawl_result['message']}"}), 500
        reviews = [item['comment'] for item in crawl_result['data'] if item.get('comment')]
        if not reviews:
            return jsonify({"error": "Không có bình luận hợp lệ"}), 500
        summary = summarize_reviews(reviews)
        sentiments = analyze_sentiments(reviews)
        chart_path = plot_sentiment_chart(sentiments)
        review_text = generate_product_review(reviews, sentiments)
        return jsonify({
            "summary": summary,
            "sentiments": sentiments,
            "chart_url": f"/static/{os.path.basename(chart_path)}",
            "product_review": review_text
        })
    # nếu là câu hỏi về nền tảng thì dùng mô hình sinh văn bản tiếng Việt để trả lời
    answer = answer_shopee_question(query)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
