from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.retriever import load_data, ChatbotSession
from app.generator import generate_answer
from app.summarizer import summarize_text
import uvicorn
import time
import os
import pandas as pd

app = FastAPI()
data = load_data()
chatbot = ChatbotSession(data)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    matched_question: str = None
    score: float = None
    generated: bool
    history: list

class SummarizeRequest(BaseModel):
    text: str

class CrawlRequest(BaseModel):
    product_url: str
    review_file: str = None  # path of file csv or xlsx (optional)

class CrawlProgress(BaseModel):
    progress: int
    message: str

class Review(BaseModel):
    username: str
    rating: int
    comment: str

class CrawlResult(BaseModel):
    progress: int
    message: str
    reviews: List[Review]
    summary: str
    overall_evaluation: str

# Fake review data
FAKE_REVIEWS = [
    {"username": "user1", "rating": 5, "comment": "Sản phẩm rất tốt, giao hàng nhanh."},
    {"username": "user2", "rating": 4, "comment": "Chất lượng ổn, đóng gói cẩn thận."},
    {"username": "user3", "rating": 3, "comment": "Tạm ổn, giá hợp lý nhưng giao hơi chậm."},
    {"username": "user4", "rating": 2, "comment": "Sản phẩm không giống mô tả, hơi thất vọng."},
    {"username": "user5", "rating": 5, "comment": "Rất hài lòng, sẽ ủng hộ lần sau."},
]

def load_reviews_from_file(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Chỉ hỗ trợ file .csv hoặc .xlsx/.xls")
    # Chuẩn hóa cột
    cols = [c.lower() for c in df.columns]
    username_col = next((c for c in cols if "user" in c or "author" in c), None)
    rating_col = next((c for c in cols if "rating" in c or "star" in c), None)
    comment_col = next((c for c in cols if "comment" in c or "review" in c or "content" in c), None)
    if not (username_col and rating_col and comment_col):
        raise ValueError("File phải có các cột: username, rating, comment (hoặc tương đương)")
    username_col = df.columns[cols.index(username_col)]
    rating_col = df.columns[cols.index(rating_col)]
    comment_col = df.columns[cols.index(comment_col)]
    reviews = []
    for _, row in df.iterrows():
        reviews.append({
            "username": str(row[username_col]),
            "rating": int(row[rating_col]),
            "comment": str(row[comment_col])
        })
    return reviews

def fake_crawl_progress():
    # fake progress crawl
    for p, msg in [(10, "Đang kiểm tra link..."),
                   (30, "Đang thu thập dữ liệu..."),
                   (60, "Đang xử lý đánh giá..."),
                   (90, "Đang tóm tắt..."),
                   (100, "Hoàn thành!")]:
        time.sleep(0.5)
        yield {"progress": p, "message": msg}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    turn = chatbot.ask(req.question, generator=generate_answer)
    return {
        "answer": turn["answer"],
        "matched_question": turn["matched_question"],
        "score": turn["score"],
        "generated": turn["generated"],
        "history": chatbot.get_history()
    }

@app.get("/chat_history")
def chat_history():
    return {"history": chatbot.get_history()}

@app.post("/reset_chat")
def reset_chat():
    chatbot.history = []
    return {"message": "Đã reset lịch sử hội thoại."}

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    summary = summarize_text(req.text)
    return {"summary": summary}

@app.post("/crawl_and_summarize", response_model=CrawlResult)
def crawl_and_summarize(req: CrawlRequest):
    # fake progress crawl
    for _ in fake_crawl_progress():
        pass  # Chỉ fake delay, không trả về từng bước
    # Nếu có file review thì đọc file, không thì dùng FAKE_REVIEWS
    if req.review_file and os.path.exists(req.review_file):
        try:
            reviews = load_reviews_from_file(req.review_file)
        except Exception as e:
            reviews = FAKE_REVIEWS
    else:
        reviews = FAKE_REVIEWS
    # Ghép comment lại để tóm tắt
    all_comments = " ".join([r["comment"] for r in reviews])
    summary = summarize_text(all_comments)
    # Đánh giá tổng quan (fake)
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    if avg_rating >= 4.5:
        overall = "Sản phẩm được đánh giá rất cao bởi người dùng."
    elif avg_rating >= 3.5:
        overall = "Sản phẩm được đánh giá khá tốt, đa số người dùng hài lòng."
    else:
        overall = "Sản phẩm nhận được nhiều ý kiến trái chiều, bạn nên cân nhắc."
    return {
        "progress": 100,
        "message": "Hoàn thành!",
        "reviews": reviews,
        "summary": summary,
        "overall_evaluation": overall
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
