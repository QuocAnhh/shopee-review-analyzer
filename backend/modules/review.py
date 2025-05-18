from pydantic import BaseModel
from typing import List
from app.summarizer import summarize_text
import os
import pandas as pd

class CrawlRequest(BaseModel):
    product_url: str
    review_file: str = None

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
    for p, msg in [(10, "Đang kiểm tra link..."),
                   (30, "Đang thu thập dữ liệu..."),
                   (60, "Đang xử lý đánh giá..."),
                   (90, "Đang tóm tắt..."),
                   (100, "Hoàn thành!")]:
        # time.sleep(0.5)  # Nếu muốn fake delay thì bỏ comment
        yield {"progress": p, "message": msg}

def crawl_and_summarize(req: CrawlRequest):
    for _ in fake_crawl_progress():
        pass
    if req.review_file and os.path.exists(req.review_file):
        try:
            reviews = load_reviews_from_file(req.review_file)
        except Exception:
            reviews = FAKE_REVIEWS
    else:
        reviews = FAKE_REVIEWS
    all_comments = " ".join([r["comment"] for r in reviews])
    summary = summarize_text(all_comments)
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    if avg_rating >= 4.5:
        overall = "Sản phẩm được đánh giá rất cao bởi người dùng."
    elif avg_rating >= 3.5:
        overall = "Sản phẩm được đánh giá khá tốt, đa số người dùng hài lòng."
    else:
        overall = "Sản phẩm nhận được nhiều ý kiến trái chiều, bạn nên cân nhắc."
    return CrawlResult(
        progress=100,
        message="Hoàn thành!",
        reviews=reviews,
        summary=summary,
        overall_evaluation=overall
    )
