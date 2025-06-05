from bson import ObjectId
from datetime import datetime

class ChatHistory:
    def __init__(self, db):
        self.collection = db.chat_history
        print(f"Initialized ChatHistory with collection: {self.collection.name}")  # Log khởi tạo

    def create_new_chat(self, user_id, initial_message=None):
        try:
            chat = {
                "user_id": user_id,
                "title": "New Chat" if not initial_message else initial_message[:50],
                "messages": [] if not initial_message else [{"content": initial_message, "role": "user", "timestamp": datetime.utcnow()}],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
            print(f"Creating new chat: {chat}")  # Log dữ liệu trước khi lưu
            result = self.collection.insert_one(chat)
            print(f"Inserted chat with ID: {result.inserted_id}")  # Log ID sau khi lưu
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error in create_new_chat: {str(e)}")
            raise e

    def update_chat(self, chat_id, user_id, messages, title=None):
        try:
            update_data = {
                "messages": messages,
                "updated_at": datetime.utcnow()
            }
            if title:
                update_data["title"] = title
            print(f"Updating chat {chat_id} with data: {update_data}")  # Log dữ liệu cập nhật
            result = self.collection.update_one(
                {"_id": ObjectId(chat_id), "user_id": user_id},
                {"$set": update_data}
            )
            print(f"Update result: matched {result.matched_count}, modified {result.modified_count}")  # Log kết quả
            return result.modified_count > 0
        except Exception as e:
            print(f"Error in update_chat: {str(e)}")
            raise e

    # Các phương thức khác giữ nguyên, chỉ thêm log tương tự nếu cần
    def get_chat_history(self, user_id):
        try:
            print(f"Fetching chat history for user_id: {user_id}")
            chats = self.collection.find({"user_id": user_id}).sort("updated_at", -1)
            chats_list = list(chats)
            print(f"Found {len(chats_list)} chats")
            return chats_list
        except Exception as e:
            print(f"Error in get_chat_history: {str(e)}")
            raise e

    def set_active_chat(self, user_id, chat_id):
        try:
            print(f"Deactivating all chats for user_id: {user_id}")
            self.collection.update_many(
                {"user_id": user_id},
                {"$set": {"is_active": False}}
            )
            print(f"Activating chat {chat_id} for user_id: {user_id}")
            result = self.collection.update_one(
                {"_id": ObjectId(chat_id), "user_id": user_id},
                {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
            )
            print(f"Set active result: modified {result.modified_count}")
            return result.modified_count > 0
        except Exception as e:
            print(f"Error in set_active_chat: {str(e)}")
            raise e

    def get_active_chat(self, user_id):
        try:
            print(f"Fetching active chat for user_id: {user_id}")
            chat = self.collection.find_one({"user_id": user_id, "is_active": True})
            print(f"Active chat: {chat}")
            return chat
        except Exception as e:
            print(f"Error in get_active_chat: {str(e)}")
            raise e

    def get_chat(self, chat_id, user_id):
        try:
            print(f"Fetching chat {chat_id} for user_id: {user_id}")
            chat = self.collection.find_one({"_id": ObjectId(chat_id), "user_id": user_id})
            print(f"Chat found: {chat}")
            return chat
        except Exception as e:
            print(f"Error in get_chat: {str(e)}")
            raise e

    def rename_chat(self, chat_id, user_id, new_title):
        try:
            print(f"Renaming chat {chat_id} to '{new_title}' for user_id: {user_id}")
            result = self.collection.update_one(
                {"_id": ObjectId(chat_id), "user_id": user_id},
                {"$set": {"title": new_title, "updated_at": datetime.utcnow()}}
            )
            print(f"Rename result: modified {result.modified_count}")
            return result.modified_count > 0
        except Exception as e:
            print(f"Error in rename_chat: {str(e)}")
            raise e

    def delete_chat(self, chat_id, user_id):
        try:
            print(f"Deleting chat {chat_id} for user_id: {user_id}")
            result = self.collection.delete_one({"_id": ObjectId(chat_id), "user_id": user_id})
            print(f"Delete result: deleted {result.deleted_count}")
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error in delete_chat: {str(e)}")
            raise e