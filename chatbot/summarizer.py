import os
import re
import unicodedata
import openai
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("cần đặt biến môi trường OPENAI_API_KEY trước khi chạy.")

openai.api_key = OPENAI_API_KEY

MODEL_NAME = "gpt-3.5-turbo" 


def preprocess_text(text):
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def call_openai(messages):
    MAX_TOTAL_CHARS = 8000
    total_chars = sum(len(m["content"]) for m in messages)
    #nếu dài quá thì cắt bớt
    if total_chars > MAX_TOTAL_CHARS:
        for m in messages:
            if m["role"] == "user" and len(m["content"]) > 2000:
                m["content"] = m["content"][:2000] + " ..."
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3
        )
        if response and response.choices:
            msg = response.choices[0].message
            if isinstance(msg, dict):
                content = msg.get("content", None)
            else:
                content = getattr(msg, "content", None)
            if content:
                return content
            else:
                print("DEBUG OpenAI API message object:", msg)
                return "Lỗi: OpenAI API trả về message không có content."
        else:
            print("DEBUG OpenAI API raw response:", response)
            return "Lỗi: Không nhận được kết quả hợp lệ từ OpenAI API."
    except Exception as e:
        print("DEBUG OpenAI API Exception:", e)
        return f"Lỗi khi gọi OpenAI API: {e}"

def preprocess_reviews(reviews, max_reviews=500, max_chars=6000):
    # Lọc bỏ comment trùng lặp, rỗng, quá ngắn hoặc chỉ chứa ký tự đặc biệt
    filtered = []
    seen = set()
    for r in reviews:
        r = preprocess_text(r)
        if len(r) < 5:
            continue
        if r in seen:
            continue
        if re.fullmatch(r"[\W_]+", r):
            continue
        seen.add(r)
        filtered.append(r)
        if len(filtered) >= max_reviews:
            break
    # Gộp lại và cắt nếu quá dài
    text = " ".join(filtered)
    if len(text) > max_chars:
        text = text[:max_chars] + " ..."
    return filtered, text

def summarize_reviews(reviews):
    if not reviews:
        return "Không có bình luận để tóm tắt."
    filtered, text = preprocess_reviews(reviews, max_reviews=500, max_chars=6000)
    prompt = (
        f"Hãy tóm tắt ngắn gọn, súc tích các bình luận sau về một sản phẩm Shopee bằng tiếng Việt:\n{text}"
    )
    messages = [
        {"role": "user", "content": prompt}
    ]
    return call_openai(messages)

def analyze_sentiments(reviews):
    # Trả về dữ liệu thô vừa crawl, không phân tích cảm xúc, không nhãn
    filtered, _ = preprocess_reviews(reviews, max_reviews=60, max_chars=2000)
    return filtered

def generate_product_review(reviews, sentiments):
    if not reviews or not sentiments:
        return "Không thể tạo nhận xét sản phẩm vào lúc này."
    filtered, text = preprocess_reviews(reviews, max_reviews=500, max_chars=6000)
    pos = sum(1 for s in sentiments if s['sentiment'] == 'positive')
    neg = sum(1 for s in sentiments if s['sentiment'] == 'negative')
    neu = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
    prompt = (
        f"Các bình luận về sản phẩm: {text}. "
        f"Có {pos} bình luận tích cực, {neu} trung tính, {neg} tiêu cực. "
        "Hãy nhận xét tổng quan sản phẩm này có đáng mua không, và giải thích lý do vì sao nên hoặc không nên mua. Trả lời ngắn gọn, súc tích, khách quan bằng tiếng Việt."
    )
    messages = [
        {"role": "user", "content": prompt}
    ]
    return call_openai(messages)

def answer_shopee_question(question):
    if not question or not isinstance(question, str):
        return "Không thể trả lời câu hỏi vào lúc này."
    prompt = (
        "Bạn là trợ lý am hiểu về sàn thương mại điện tử Shopee Việt Nam. "
        "Hãy trả lời ngắn gọn, chính xác, dễ hiểu cho câu hỏi sau bằng tiếng Việt: " + question
    )
    messages = [
        {"role": "user", "content": prompt}
    ]
    return call_openai(messages)
