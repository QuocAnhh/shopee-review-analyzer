from datetime import datetime
from bson import ObjectId

class ChatHistory:
    def __init__(self, db):
        self.db = db
        self.history = self.db.chat_history

    def create_history(self, user_id, title, messages):
        history_data = {
            "user_id": user_id,
            "title": title,
            "messages": messages,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = self.history.insert_one(history_data)
        return str(result.inserted_id)

    def get_user_history(self, user_id):
        return list(self.history.find({"user_id": user_id}).sort("updated_at", -1))

    def get_history_by_id(self, history_id, user_id):
        return self.history.find_one({"_id": ObjectId(history_id), "user_id": user_id})

    def delete_history(self, history_id, user_id):
        result = self.history.delete_one({"_id": ObjectId(history_id), "user_id": user_id})
        return result.deleted_count > 0