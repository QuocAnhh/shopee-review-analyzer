from pydantic import BaseModel
from app.retriever import load_data, ChatbotSession
from app.generator import generate_answer

faq_data = load_data()
chatbot_session = ChatbotSession(faq_data)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    matched_question: str = None
    score: float = None
    generated: bool
    history: list

class Chatbot:
    def __init__(self, session):
        self.session = session

    def chat(self, req: ChatRequest):
        turn = self.session.ask(req.question, generator=generate_answer)
        return ChatResponse(
            answer=turn["answer"],
            matched_question=turn["matched_question"],
            score=turn["score"],
            generated=turn["generated"],
            history=self.session.get_history()
        )

    def get_history(self):
        return {"history": self.session.get_history()}

    def reset_history(self):
        self.session.history = []
        return {"message": "Đã reset lịch sử hội thoại."}

chatbot = Chatbot(chatbot_session)
