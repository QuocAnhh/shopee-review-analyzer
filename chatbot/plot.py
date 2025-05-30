import uuid
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CHART_DIR = Path("charts")
CHART_DIR.mkdir(parents=True, exist_ok=True)

def plot_sentiment_chart(sentiments):
    """Tạo biểu đồ pie chart đẹp cho phân tích cảm xúc"""
    labels = ['Tích cực', 'Trung tính', 'Tiêu cực']
    raw_labels = [s['sentiment'] for s in sentiments]
    counts = [
        raw_labels.count('positive'),
        raw_labels.count('neutral'), 
        raw_labels.count('negative')
    ]
      # Tạo figure với pie chart duy nhất - kích thước vừa phải
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.suptitle('Phân tích cảm xúc bình luận sản phẩm Shopee', fontsize=14, fontweight='bold')
    
    # Pie chart 
    colors = ['#2ecc71', '#95a5a6', '#e74c3c'] 
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"{int(round(pct/100.*sum(counts)))}\n({pct:.1f}%)" if pct > 0 else '',
        startangle=90,
        explode=(0.05, 0, 0.05),  # explode positive and negative
        shadow=True, textprops={'fontsize': 10, 'fontweight': 'bold'}
    )
    ax.set_title('Phân bố cảm xúc', fontweight='bold', pad=15, fontsize=12)
    
    plt.tight_layout()
    filename = f"sentiment_analysis_{uuid.uuid4().hex[:8]}.png"
    out_path = CHART_DIR / filename
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    return str(out_path)
