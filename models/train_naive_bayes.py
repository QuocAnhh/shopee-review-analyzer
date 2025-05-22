import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

os.makedirs("models", exist_ok=True)
MODEL_PATH = "models/naive_bayes_sentiment.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

# support đọc cả .csv và .txt (dạng text,sentiment)
def load_data(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext == ".txt":
        df = pd.read_csv(filepath, delimiter=",", header=0)
    else:
        raise ValueError("Chỉ hỗ trợ file .csv hoặc .txt")
    return df

data_file = "sentiment_data.csv"  # hoặc ".txt"
df = load_data(data_file)

df['text'] = df['text'].astype(str).str.strip()

X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['sentiment'], test_size=0.2, random_state=42, stratify=df['sentiment']
)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))

joblib.dump(clf, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)
print(f"Đã lưu model vào {MODEL_PATH} và vectorizer vào {VECTORIZER_PATH}")

