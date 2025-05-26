from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, db):
        self.db = db
        self.users = self.db.users

    def create_user(self, name, email, password_hash):
        user_data = {
            "name": name,
            "email": email,
            "password": password_hash,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = self.users.insert_one(user_data)
        return str(result.inserted_id)

    def find_user_by_email(self, email):
        return self.users.find_one({"email": email})

    def find_user_by_id(self, user_id):
        return self.users.find_one({"_id": ObjectId(user_id)})