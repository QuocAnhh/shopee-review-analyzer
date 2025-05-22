async function askShopee() {
    const query = document.getElementById('query').value;
    document.getElementById('result').innerHTML = 'Đang xử lý...';
    document.getElementById('chart').innerHTML = '';
    const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    });
    const data = await res.json();
    if (data.error) {
        document.getElementById('result').innerHTML = data.error;
        return;
    }
    // Nếu là kết quả phân tích sản phẩm
    if (data.summary && (data.demo_reviews || data.file_path)) {
        let html = `<b>Tóm tắt:</b> <br>${data.summary}<br><br>`;
        if (data.file_path) {
            html += `<b>File dữ liệu crawl:</b> <a href='${data.file_path}' download target='_blank'>Tải file dữ liệu vừa crawl</a><br><br>`;
        }
        if (data.demo_reviews && data.demo_reviews.length > 0) {
            html += '<b>Demo cảm xúc (5 bình luận ngẫu nhiên):</b><ul>';
            data.demo_reviews.forEach(function(s) {
                html += `<li>${s.review ? s.review : ''} <b>[${s.sentiment}]</b></li>`;
            });
            html += '</ul>';
        }
        if (data.product_review) {
            html += `<br><b>Đánh giá tổng quan:</b><br>${data.product_review}`;
        }
        document.getElementById('result').innerHTML = html;
        if (data.chart_url) {
            document.getElementById('chart').innerHTML = `<img src='${data.chart_url}' style='max-width:400px;'>`;
        } else {
            document.getElementById('chart').innerHTML = '';
        }
    } else if (data.answer) {
        // Nếu là trả lời câu hỏi Shopee
        document.getElementById('result').innerHTML = `<b>Trả lời:</b><br>${data.answer}`;
        document.getElementById('chart').innerHTML = '';
    }
}
