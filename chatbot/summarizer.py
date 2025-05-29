import os
import re
import unicodedata
import openai
from dotenv import load_dotenv
from collections import Counter
from typing import List, Dict, Tuple


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
    """Updated summarize_reviews with highlights"""
    highlighted_summary, keywords = summarize_reviews_with_highlights(reviews)
    return highlighted_summary

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

def answer_shopee_question(question, chat_history=None):
    if not question or not isinstance(question, str):
        return "Không thể trả lời câu hỏi vào lúc này."
    
    # Tạo context từ lịch sử chat
    context = ""
    if chat_history and len(chat_history) > 0:
        # Lấy 3 tin nhắn gần nhất để làm context
        recent_history = chat_history[-3:]
        context_parts = []
        for entry in recent_history:
            if 'user' in entry and 'bot' in entry:
                context_parts.append(f"User: {entry['user']}")
                context_parts.append(f"Assistant: {entry['bot']}")
        if context_parts:
            context = "\n\nLịch sử cuộc hội thoại:\n" + "\n".join(context_parts) + "\n\n"
    
    prompt = (
        "Bạn là trợ lý am hiểu về sàn thương mại điện tử Shopee Việt Nam. "
        f"{context}"
        "Dựa vào ngữ cảnh cuộc hội thoại trên (nếu có), hãy trả lời ngắn gọn, chính xác, dễ hiểu cho câu hỏi sau bằng tiếng Việt: " + question
    )
    messages = [
        {"role": "user", "content": prompt}
    ]
    return call_openai(messages)

def extract_keywords(text, top_n=10):
    """Trích xuất từ khóa quan trọng từ text sử dụng OpenAI"""
    if not text or len(text.strip()) < 10:
        return []
    
    # Rút gọn text nếu quá dài
    if len(text) > 4000:
        text = text[:4000] + "..."
    
    prompt = f"""
Phân tích đoạn text review sản phẩm sau và trích xuất các từ khóa/cụm từ quan trọng nhất 
liên quan đến CHẤT LƯỢNG, TÍNH NĂNG, và ĐÁNH GIÁ sản phẩm.

Text: {text}

Hãy trả về {top_n} từ khóa/cụm từ quan trọng nhất, mỗi từ khóa trên một dòng, 
chỉ trả về từ khóa thuần túy, không giải thích thêm.
Ưu tiên các từ khóa thể hiện:
- Chất lượng sản phẩm (tốt, xấu, bền, mỏng, chắc chắn...)
- Tính năng (đẹp, tiện lợi, dễ sử dụng...)
- Cảm xúc về sản phẩm (hài lòng, thất vọng, ưng ý...)
- Giá cả (rẻ, đắt, xứng đáng...)

Ví dụ format trả về:
chất lượng tốt
giá rẻ
đẹp
bền chắc
hài lòng
"""
    
    try:
        messages = [{"role": "user", "content": prompt}]
        response = call_openai(messages)
        
        if response and not response.startswith("Lỗi"):
            # Parse response
            keywords = []
            lines = response.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('-') and not line.startswith('*'):
                    # Loại bỏ số thứ tự nếu có
                    if '. ' in line:
                        line = line.split('. ', 1)[1]
                    keywords.append((line.lower(), 1))  # Tần suất giả định là 1
            
            return keywords[:top_n]
        else:
            # Fallback to original method
            return extract_keywords_fallback(text, top_n)
    except Exception as e:
        print(f"Error in AI keyword extraction: {e}")
        return extract_keywords_fallback(text, top_n)

def extract_keywords_fallback(text, top_n=10):
    """Phương pháp fallback để trích xuất từ khóa"""
    # Danh sách từ dừng tiếng Việt
    stop_words = {
        'và', 'của', 'có', 'là', 'trong', 'với', 'được', 'để', 'một', 'này', 
        'đó', 'những', 'các', 'cho', 'từ', 'về', 'sẽ', 'cũng', 'như', 'mà',
        'đã', 'hay', 'thì', 'nó', 'bị', 'người', 'tôi', 'mình', 'em', 'anh',
        'chị', 'ông', 'bà', 'rất', 'lắm', 'quá', 'nữa', 'vẫn', 'còn', 'đang',
        'shop', 'seller', 'shipper', 'đơn', 'hàng', 'order', 'mua', 'bán',
        'giao', 'nhận', 'ship', 'fast', 'nhanh', 'chậm', 'lâu', 'sớm'
    }
    
    # Từ khóa quan trọng cho review sản phẩm
    important_patterns = [
        r'chất lượng \w+', r'giá \w+', r'màu \w+', r'kích thước \w+',
        r'thiết kế \w+', r'đóng gói \w+', r'giao hàng \w+',
        r'tốt', r'xấu', r'đẹp', r'chắc', r'bền', r'mỏng', r'dày',
        r'hài lòng', r'thất vọng', r'ưng ý', r'rẻ', r'đắt'
    ]
    
    keywords = []
    text = text.lower()
    
    # Tìm các pattern quan trọng
    for pattern in important_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if match not in [kw[0] for kw in keywords]:
                freq = text.count(match)
                keywords.append((match, freq))
    
    # Sắp xếp theo tần suất
    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords[:top_n]

def highlight_keywords_in_text(text, keywords):
    """Highlight từ khóa trong text với styling nâng cao"""
    highlighted_text = text
    
    # Sắp xếp keywords theo độ dài giảm dần để tránh conflict
    sorted_keywords = sorted(keywords, key=lambda x: len(str(x[0])), reverse=True)
    
    for keyword, freq in sorted_keywords:
        keyword_str = str(keyword)
        # Tạo pattern để match whole words hoặc phrases
        if ' ' in keyword_str:  # Cụm từ
            pattern = re.compile(r'\b' + re.escape(keyword_str) + r'\b', re.IGNORECASE)
        else:  # Từ đơn
            pattern = re.compile(r'\b' + re.escape(keyword_str) + r'\b', re.IGNORECASE)
        
        # Highlight với class CSS để dễ styling
        highlight_class = 'keyword-highlight'
        if freq >= 5:  # Từ xuất hiện nhiều
            highlight_class = 'keyword-highlight-high'
        elif freq >= 3:  # Từ xuất hiện vừa
            highlight_class = 'keyword-highlight-medium'
        
        replacement = f'<span class="{highlight_class}" data-freq="{freq}">{keyword_str}</span>'
        highlighted_text = pattern.sub(replacement, highlighted_text)
    
    return highlighted_text

def analyze_review_keywords(reviews):
    """Phân tích từ khóa trong reviews và highlight"""
    all_text = " ".join(reviews)
    keywords = extract_keywords(all_text, top_n=15)
    
    highlighted_reviews = []
    for review in reviews:
        highlighted = highlight_keywords_in_text(review, keywords[:10])
        highlighted_reviews.append(highlighted)
    
    return highlighted_reviews, keywords

def summarize_reviews_with_highlights(reviews):
    """Tóm tắt reviews và highlight từ khóa quan trọng"""
    if not reviews:
        return "Không có bình luận để tóm tắt.", []
    
    filtered, text = preprocess_reviews(reviews, max_reviews=500, max_chars=6000)
    
    # Tạo summary
    prompt = (
        f"Hãy tóm tắt ngắn gọn, súc tích các bình luận sau về một sản phẩm Shopee bằng tiếng Việt:\n{text}"
    )
    messages = [{"role": "user", "content": prompt}]
    summary = call_openai(messages)
    
    # Trích xuất từ khóa và highlight
    keywords = extract_keywords(text, top_n=10)
    highlighted_summary = highlight_keywords_in_text(summary, keywords)
    
    return highlighted_summary, keywords

def get_sentiment_keywords(reviews_with_sentiment):
    """Trích xuất từ khóa theo từng cảm xúc"""
    positive_text = " ".join([r['review'] for r in reviews_with_sentiment if r['sentiment'] == 'positive'])
    negative_text = " ".join([r['review'] for r in reviews_with_sentiment if r['sentiment'] == 'negative'])
    
    positive_keywords = extract_keywords(positive_text, top_n=10)
    negative_keywords = extract_keywords(negative_text, top_n=10)
    
    return {
        'positive': positive_keywords,
        'negative': negative_keywords
    }

def highlight_reviews_by_sentiment(reviews_with_sentiment):
    """Highlight từ khóa trong reviews theo cảm xúc"""
    sentiment_keywords = get_sentiment_keywords(reviews_with_sentiment)
    
    highlighted_reviews = []
    for review_data in reviews_with_sentiment:
        review = review_data['review']
        sentiment = review_data['sentiment']
        
        if sentiment == 'positive':
            keywords = sentiment_keywords['positive'][:5]
        elif sentiment == 'negative':
            keywords = sentiment_keywords['negative'][:5]
        else:
            keywords = []
        
        highlighted = highlight_keywords_in_text(review, keywords)
        highlighted_reviews.append({
            'review': highlighted,
            'sentiment': sentiment,
            'original': review_data['review']
        })
    
    return highlighted_reviews

def extract_product_features(reviews):
    """Trích xuất các tính năng/đặc điểm sản phẩm được nhắc đến"""
    # Từ khóa đặc trưng cho sản phẩm
    feature_patterns = [
        r'chất lượng\s+\w+', r'màu\s+\w+', r'kích thước\s+\w+', 
        r'giá\s+\w+', r'đóng gói\s+\w+', r'giao hàng\s+\w+',
        r'thiết kế\s+\w+', r'tính năng\s+\w+', r'hiệu năng\s+\w+'
    ]
    
    all_text = " ".join(reviews).lower()
    features = []
    
    for pattern in feature_patterns:
        matches = re.findall(pattern, all_text)
        features.extend(matches)
    
    # Trích xuất từ khóa chung
    general_keywords = extract_keywords(all_text, top_n=20)
    
    return {
        'specific_features': list(set(features)),
        'general_keywords': general_keywords
    }

def get_crawled_data_info(reviews):
    """Trả về thông tin về dữ liệu đã crawl"""
    if not reviews:
        return {
            'total_reviews': 0,
            'sample_reviews': [],
            'data_quality': 'Không có dữ liệu',
            'file_info': 'Chưa có file dữ liệu'
        }
    
    # Lọc và làm sạch dữ liệu
    filtered, _ = preprocess_reviews(reviews, max_reviews=len(reviews))
    
    # Thống kê cơ bản
    total_reviews = len(filtered)
    avg_length = sum(len(review) for review in filtered) / total_reviews if total_reviews > 0 else 0
    
    # Lấy mẫu một số reviews
    sample_size = min(3, total_reviews)
    sample_reviews = filtered[:sample_size]
    
    # Đánh giá chất lượng dữ liệu
    if total_reviews >= 50:
        data_quality = "Tốt - Đủ dữ liệu để phân tích"
    elif total_reviews >= 20:
        data_quality = "Khá - Dữ liệu vừa đủ"
    elif total_reviews >= 10:
        data_quality = "Trung bình - Dữ liệu ít"
    else:
        data_quality = "Yếu - Dữ liệu không đủ"
    
    return {
        'total_reviews': total_reviews,
        'average_length': round(avg_length, 1),
        'sample_reviews': sample_reviews,
        'data_quality': data_quality,
        'file_info': f'Đã crawl thành công {total_reviews} reviews'
    }

def get_demo_reviews_with_highlights(reviews_with_sentiment):
    """Lấy 5 reviews tích cực và 5 reviews tiêu cực với keyword highlighting"""
    print(f"DEBUG get_demo_reviews_with_highlights: Input length: {len(reviews_with_sentiment) if reviews_with_sentiment else 0}")
    
    if not reviews_with_sentiment:
        return {
            'positive_reviews': [],
            'negative_reviews': [],
            'keywords_analysis': {}
        }
    
    # Phân loại reviews theo sentiment
    positive_reviews = [r for r in reviews_with_sentiment if r.get('sentiment') == 'positive']
    negative_reviews = [r for r in reviews_with_sentiment if r.get('sentiment') == 'negative']
    
    # Lấy tối đa 5 reviews mỗi loại
    demo_positive = positive_reviews[:5]
    demo_negative = negative_reviews[:5]
    
    # Trích xuất keywords riêng cho mỗi nhóm
    positive_text = " ".join([r['review'] for r in demo_positive])
    negative_text = " ".join([r['review'] for r in demo_negative])
    
    positive_keywords = extract_keywords(positive_text, top_n=8)
    negative_keywords = extract_keywords(negative_text, top_n=8)
    
    # Highlight keywords trong reviews
    highlighted_positive = []
    for review_data in demo_positive:
        highlighted = highlight_keywords_in_text(review_data['review'], positive_keywords)
        highlighted_positive.append({
            'original': review_data['review'],
            'highlighted': highlighted,
            'sentiment': review_data['sentiment']
        })
    
    highlighted_negative = []
    for review_data in demo_negative:
        highlighted = highlight_keywords_in_text(review_data['review'], negative_keywords)
        highlighted_negative.append({
            'original': review_data['review'],
            'highlighted': highlighted,
            'sentiment': review_data['sentiment']
        })
    
    return {
        'positive_reviews': highlighted_positive,
        'negative_reviews': highlighted_negative,
        'keywords_analysis': {
            'positive_keywords': positive_keywords,
            'negative_keywords': negative_keywords
        }
    }

def generate_overall_assessment(reviews, sentiments, summary, keywords):
    """Tạo đánh giá tổng thể cuối cùng về sản phẩm"""
    print(f"DEBUG generate_overall_assessment: reviews={len(reviews) if reviews else 0}, sentiments={len(sentiments) if sentiments else 0}")
    
    if not reviews or not sentiments:
        return {
            'overall_score': 0,
            'recommendation': 'Không thể đánh giá',
            'key_points': [],
            'detailed_analysis': 'Không đủ dữ liệu để phân tích',
            'buying_advice': 'Cần thêm thông tin'
        }
    
    # Tính điểm tổng thể
    pos_count = sum(1 for s in sentiments if s.get('sentiment') == 'positive')
    neg_count = sum(1 for s in sentiments if s.get('sentiment') == 'negative')
    neu_count = sum(1 for s in sentiments if s.get('sentiment') == 'neutral')
    total_count = len(sentiments)
    
    if total_count == 0:
        return {
            'overall_score': 0,
            'recommendation': 'Không thể đánh giá',
            'key_points': [],
            'detailed_analysis': 'Không có dữ liệu sentiment',
            'buying_advice': 'Cần thêm thông tin'
        }
    
    # Tính điểm từ 1-10
    positive_ratio = pos_count / total_count
    negative_ratio = neg_count / total_count
    overall_score = round((positive_ratio * 10) - (negative_ratio * 3), 1)
    overall_score = max(1, min(10, overall_score))  # Giới hạn 1-10
    
    # Xác định recommendation
    if overall_score >= 8:
        recommendation = "Rất đáng mua"
        advice_tone = "tích cực"
    elif overall_score >= 6:
        recommendation = "Đáng mua"
        advice_tone = "khuyến khích"
    elif overall_score >= 4:
        recommendation = "Cân nhắc kỹ"
        advice_tone = "thận trọng"
    else:
        recommendation = "Không nên mua"
        advice_tone = "không khuyến khích"
    
    # Trích xuất điểm chính từ keywords
    key_points = []
    if keywords:
        top_keywords = [kw[0] for kw in keywords[:5]]
        key_points = [f"Được nhắc đến nhiều: {', '.join(top_keywords)}"]
    
    if pos_count > 0:
        key_points.append(f"{pos_count} người dùng hài lòng ({round(positive_ratio*100, 1)}%)")
    if neg_count > 0:
        key_points.append(f"{neg_count} người dùng không hài lòng ({round(negative_ratio*100, 1)}%)")
    
    # Tạo phân tích chi tiết bằng AI
    analysis_prompt = (
        f"Dựa vào dữ liệu phân tích: {pos_count} reviews tích cực, {neu_count} trung tính, {neg_count} tiêu cực. "
        f"Điểm tổng thể: {overall_score}/10. Keywords chính: {', '.join([kw[0] for kw in keywords[:5]] if keywords else [])}. "
        f"Tóm tắt: {summary[:200]}... "
        "Hãy viết một đánh giá chi tiết ngắn gọn (2-3 câu) về sản phẩm này bằng tiếng Việt."
    )
    
    detailed_analysis = call_openai([{"role": "user", "content": analysis_prompt}])
    
    # Lời khuyên mua hàng
    buying_advice_prompt = (
        f"Với điểm số {overall_score}/10 và xu hướng {advice_tone}, "
        f"hãy đưa ra lời khuyên ngắn gọn (1-2 câu) cho người muốn mua sản phẩm này. "
        "Trả lời bằng tiếng Việt, thực tế và hữu ích."
    )
    
    buying_advice = call_openai([{"role": "user", "content": buying_advice_prompt}])
    
    return {
        'overall_score': overall_score,
        'recommendation': recommendation,
        'key_points': key_points,
        'detailed_analysis': detailed_analysis,
        'buying_advice': buying_advice,
        'sentiment_distribution': {
            'positive': pos_count,
            'neutral': neu_count,
            'negative': neg_count,
            'total': total_count
        }
    }
