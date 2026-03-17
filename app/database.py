from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGODB_URL)
db     = client[settings.DB_NAME]

users_col        = db["users"]       
websites_col     = db["websites"]     
chat_col         = db["chat_history"] 

def save_chat(user_id: str, message: str, response: str):
    chat_col.insert_one({
        "user_id":  user_id,
        "message":  message,
        "response": response,
    })
