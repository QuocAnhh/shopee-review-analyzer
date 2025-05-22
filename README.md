# Shopee Review Analyzer

## Giới thiệu

Shopee Review Analyzer là công cụ crawl, tóm tắt, phân tích cảm xúc và trực quan hóa bình luận sản phẩm Shopee. Hỗ trợ hỏi đáp về sản phẩm hoặc Shopee bằng AI (OpenAI GPT).

## Cấu trúc thư mục

```
shopee-review-analyzer/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── crawled_data/           # Thư mục lưu file dữ liệu bình luận đã crawl (xlsx/txt)
├── charts/                 # Thư mục lưu ảnh biểu đồ cảm xúc
├── static/                 # Thư mục chứa file tĩnh (index.html, script.js, style.css)
├── chatbot/                # Xử lý NLP, AI (summarizer.py, plot.py, ...)
├── crawl/                  # Code crawl dữ liệu Shopee (crawl_api.py, ...)
└── ...
```

## Hướng dẫn cài đặt & chạy

### 1. Yêu cầu hệ thống
- Python >= 3.11
- pip (Python package manager)

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Thiết lập API Key (OpenAI, Shopee)
- Tạo file `.env`:
  ```env
  OPENAI_API_KEY=sk-xxxxxxx
  SHOPEE_API_URL=https://shopee.vn/xxx/vx/xxx/xxx
 
  ```
- **Không commit file `.env` lên GitHub!**
- Nếu deploy server, chỉ cần đặt biến môi trường tương ứng.

### 4. Chạy ứng dụng
```bash
python main.py
```

### 5. Truy cập giao diện web
- Mở trình duyệt và truy cập: [http://localhost:5000](http://localhost:5000)

## Hướng dẫn sử dụng
- Nhập link sản phẩm Shopee hoặc câu hỏi về Shopee vào ô nhập và nhấn "Gửi".
- Xem kết quả tóm tắt, phân tích cảm xúc, biểu đồ cảm xúc, file dữ liệu crawl và trả lời tự động.
- Có thể tải file dữ liệu bình luận đã crawl về máy.

## Đóng góp & phát triển
1. Fork hoặc clone repo về máy:
   ```bash
   git clone https://github.com/QuocAnhh/shopee-review-analyzer.git
   ```
2. Tạo nhánh mới cho từng tính năng (optional):
   ```bash
   git checkout -b feature/ten-tinh-nang
   ```
3. Commit và push code:
   ```bash
   git add .
   git commit -m "Mô tả thay đổi"
   git push origin feature/ten-tinh-nang hoặc git push origin main
   ```
4. Mở Pull Request để review và merge vào main.

## Lưu ý
- Không push file `.env`, dữ liệu crawl lên GitHub.

---

**Mọi thắc mắc hoặc đóng góp vui lòng mở issue hoặc liên hệ trực tiếp qua GitHub.**
