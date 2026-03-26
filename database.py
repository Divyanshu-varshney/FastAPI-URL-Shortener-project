from pymongo import MongoClient

# Database name → url_shortener
# Collection → urls

client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
collection = db["urls"]
