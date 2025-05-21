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
    if (data.summary && data.sentiments) {
        let html = `<b>Tóm tắt:</b> <br>${data.summary}<br><br>`;
        html += '<b>Phân tích cảm xúc:</b><ul>';
        data.sentiments.forEach(function(s) {
            html += `<li>${s.review ? s.review : ''} <b>[${s.sentiment}]</b></li>`;
        });
        html += '</ul>';
        if (data.product_review) {
            html += `<br><b>Đánh giá tổng quan:</b><br>${data.product_review}`;
        }
        document.getElementById('result').innerHTML = html;
        document.getElementById('chart').innerHTML = `<img src='${data.chart_url}' style='max-width:400px;'>`;
    } else if (data.answer) {
        // Nếu là trả lời câu hỏi Shopee
        document.getElementById('result').innerHTML = `<b>Trả lời:</b><br>${data.answer}`;
    }
}
