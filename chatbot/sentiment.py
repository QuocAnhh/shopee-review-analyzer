from textblob import TextBlob

def analyze_sentiment(reviews):
    results = []
    for review in reviews:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"
        results.append({"review": review, "sentiment": label, "score": polarity})
    return results
