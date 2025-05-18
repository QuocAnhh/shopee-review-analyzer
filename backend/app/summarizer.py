from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    # Nếu text quá ngắn thì trả về luôn
    if len(text.split()) < 20:
        return text
    result = summarizer(text, max_length=60, min_length=10, do_sample=False)
    return result[0]['summary_text']
