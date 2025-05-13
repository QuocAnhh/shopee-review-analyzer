from summa.summarizer import summarize

def summarize_review(text, ratio=0.3):
    try:
        return summarize(text, ratio=ratio)
    except:
        return ""

def summarize_all(df, column='clean_comments'):
    df['summary'] = df[column].apply(lambda x: summarize_review(x, ratio=0.3))
    return df