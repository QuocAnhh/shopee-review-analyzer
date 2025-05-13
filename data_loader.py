import pandas as pd

def load_reviews(path='processed_shopee_reviews.csv'):
    df = pd.read_csv(path)
    df = df.dropna(subset=['clean_comments'])
    return df