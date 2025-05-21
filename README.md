# Shopee Review Analyzer

## Hướng dẫn chạy project

### 1. Cài đặt môi trường
- Python 3.11+
- Cài các thư viện cần thiết:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Chuẩn bị mô hình
- Đăng nhập HuggingFace CLI:
  ```bash
  huggingface-cli login
  ```
- Đảm bảo đã có file mô hình sentiment (Naive Bayes) và vectorizer trong thư mục `models/`:
  - `models/naive_bayes_sentiment.pkl`
  - `models/vectorizer.pkl`
- Lần đầu chạy sẽ tự động tải các model từ HuggingFace

### 3. Chạy server Flask
```bash
python main.py
```

### 4. Truy cập giao diện
- Mở trình duyệt và truy cập: [http://localhost:5000](http://localhost:5000)

### 5. Sử dụng
- Nhập link sản phẩm Shopee hoặc câu hỏi về Shopee vào ô nhập và nhấn "Gửi".
- Xem kết quả tóm tắt, phân tích cảm xúc, biểu đồ và trả lời tự động.

---

**Lưu ý:**  
- Nếu gặp lỗi quyền truy cập model HuggingFace, hãy "Request access" trên trang model và kiểm tra lại token.
- Nếu thiếu mô hình sentiment, hãy train và lưu lại bằng scikit-learn.

## Contribute
Các bạn làm theo như bên dưới để làm việc nhóm với repo này

1. Clone repo về máy (`git clone https://github.com/QuocAnhh/shopee-review-analyzer.git`)
2. Tạo nhánh làm việc của từng người (ai làm frontend, backend thì 1 nhánh, ai train model thì 1 nhánh,...) (`git checkout -b feature/ten-tinh-nang`)
3. Làm việc và commit các thay đổi (`git add .`) (`git commit -m 'Add some amazing feature'`)
4. Push lên branch mà đã tạo trước đó (`git push origin feature/ten-tinh-nang`)
5. Mở Pull Request để review code và merge vào main
