import os
import re
import unicodedata
from transformers import pipeline
import joblib

summarizer = pipeline("text2text-generation", model="pengold/t5-vietnamese-summarization", max_length=128)

def preprocess_text(text):
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def summarize_reviews(reviews):
    # gộp các review thành một đoạn văn
    text = " ".join([preprocess_text(r) for r in reviews])
    # tóm tắt
    result = summarizer(text)
    if result and 'generated_text' in result[0]:
        return result[0]['generated_text']
    elif result and 'summary_text' in result[0]:
        return result[0]['summary_text']
    else:
        return "Không thể tóm tắt các bình luận."

# Sentiment với Naive Bayes
sentiment_model = joblib.load("models/naive_bayes_sentiment.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def predict_sentiment(text):
    # Tiền xử lý giống lúc train
    text = preprocess_text(text)
    X = vectorizer.transform([text])
    pred = sentiment_model.predict(X)[0]
    return pred

def analyze_sentiments(reviews):
    # Trả về list dict
    return [{"review": r, "sentiment": predict_sentiment(r)} for r in reviews]

# sinh văn bản tiếng việt
from transformers import pipeline as gen_pipeline

text_generator = gen_pipeline("text-generation", model="bkai-foundation-models/vietnamese-llama2-7b-40GB", max_new_tokens=150)

def generate_product_review(reviews, sentiments):
    """Sinh ra đoạn đánh giá tổng quan sản phẩm có đáng mua không, vì sao."""
    pos = sum(1 for s in sentiments if s['sentiment'] == 'positive')
    neg = sum(1 for s in sentiments if s['sentiment'] == 'negative')
    neu = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
    prompt = (
        f"Các bình luận về sản phẩm: {' | '.join(reviews)}. "
        f"Có {pos} bình luận tích cực, {neu} trung tính, {neg} tiêu cực. "
        "Hãy nhận xét tổng quan sản phẩm này có đáng mua không, và giải thích lý do vì sao nên hoặc không nên mua. Trả lời ngắn gọn, súc tích, khách quan."
    )
    response = text_generator(prompt)
    if response and "generated_text" in response[0]:
        return response[0]["generated_text"].strip()
    else:
        return "Không thể sinh nhận xét tổng quan."

def answer_shopee_question(question):
    """Trả lời các câu hỏi về Shopee bằng mô hình tiếng Việt."""
    prompt = (
        "Bạn là trợ lý am hiểu về sàn thương mại điện tử Shopee Việt Nam. "
        "Hãy trả lời ngắn gọn, chính xác, dễ hiểu cho câu hỏi sau: " + question
    )
    response = text_generator(prompt)
    if response and "generated_text" in response[0]:
        return response[0]["generated_text"].strip()
    else:
        return "Không thể trả lời câu hỏi"
