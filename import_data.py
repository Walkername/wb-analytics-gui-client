import pymongo
import json

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "wb-products"
COLLECTION_NAME = "products"
IMPORT_FILE = "imported_data.json"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Load data from the JSON file
with open(IMPORT_FILE, "r", encoding="utf-8") as file:
    documents = json.load(file)

#for doc in documents:
#    print(doc)

# Insert the documents into the collection
if isinstance(documents, list):
    collection.insert_many(documents)
    print(f"Inserted {len(documents)} documents into the collection '{COLLECTION_NAME}'.")
else:
    collection.insert_one(documents)
    print(f"Inserted one document into the collection '{COLLECTION_NAME}'.")
