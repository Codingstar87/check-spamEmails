from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)
db = client["user_database"]

user_collection = db["users"]
session_collection = db["sessions"]
spam_emails_list = db["Spam-email"]
spam_domain_list = db["Spam-domain"]
