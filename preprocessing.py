from underthesea import word_tokenize
import re

def clean_text(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def tokenize_vi(text):
    return word_tokenize(text, format="text").split()

def preprocess_reviews(df, column='clean_comments'):
    df['cleaned'] = df[column].apply(clean_text)
    df['tokens'] = df['cleaned'].apply(tokenize_vi)
    return df