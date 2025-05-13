from data_loader import load_reviews
from preprocessing import preprocess_reviews
from topic_modeling import build_lda_model, show_topics, visualize_lda
from summarizer import summarize_all

def main():
    df = load_reviews('processed_shopee_reviews.csv')
    df = preprocess_reviews(df, column='clean_comments')

    lda_model, corpus, dictionary = build_lda_model(df['tokens'].tolist(), num_topics=5)
    show_topics(lda_model)
    visualize_lda(lda_model, corpus, dictionary)

    df = summarize_all(df, column='clean_comments')
    df[['clean_comments', 'summary']].to_csv('output_summary.csv', index=False)
    print("Hoàn thành. File kết quả: output_summary.csv, LDA visualization: lda_vietnamese.html")

if __name__ == '__main__':
    main()