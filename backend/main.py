from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from modules.chatbot import chatbot, ChatRequest, ChatResponse
from modules.review import crawl_and_summarize, CrawlRequest, CrawlResult

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return chatbot.chat(req)

@app.get("/chat_history")
def chat_history():
    return chatbot.get_history()

@app.post("/reset_chat")
def reset_chat():
    return chatbot.reset_history()

@app.post("/crawl_and_summarize", response_model=CrawlResult)
def crawl_and_summarize_api(req: CrawlRequest):
    return crawl_and_summarize(req)
