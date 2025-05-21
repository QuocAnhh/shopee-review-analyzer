import matplotlib.pyplot as plt
import os
import uuid

def plot_sentiment_chart(sentiments):
    labels = ['Tích cực', 'Trung tính', 'Tiêu cực']
    raw_labels = [s['sentiment'] for s in sentiments]
    counts = [
        raw_labels.count('positive'),
        raw_labels.count('neutral'),
        raw_labels.count('negative')
    ]
    colors = ['green', 'gray', 'red']
    plt.figure(figsize=(5, 4))
    plt.pie(
        counts,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"{int(round(pct/100.*sum(counts)))} ({pct:.1f}%)" if pct > 0 else '',
        startangle=90,
        counterclock=False
    )
    plt.title('Tỉ lệ cảm xúc bình luận')
    plt.tight_layout()
    filename = f"sentiment_{uuid.uuid4().hex[:8]}.png"
    out_path = os.path.join('C:/Users/ADMIN/shopee-review-analyzer/static', filename)
    plt.savefig(out_path)
    plt.close()
    return out_path
