import pymongo
import json

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "wb-products"
COLLECTION_NAME = "products"
EXPORT_FILE = "exported_data.json"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Fetch all documents
documents = list(collection.find())

# Remove the MongoDB "_id" field if needed (optional)
for doc in documents:
    doc.pop("_id", None)

# Export to a JSON file
with open(EXPORT_FILE, "w", encoding="utf-8") as file:
    json.dump(documents, file, indent=4, ensure_ascii=False)

print(f"Data exported successfully to {EXPORT_FILE}")
