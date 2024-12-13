import pymongo
from config.config import MONGO_URI, MONGO_CONFIG

class DBService:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000) # 3 sec to connect
        self.db = self.client[MONGO_CONFIG["database"]]
        self.collection = self.db["products"]
    
    def is_connected(self):
        """Check if the database connection is active."""
        if not self.client:
            return False
        try:
            self.client.server_info()
            return True
        except pymongo.errors.ServerSelectionTimeoutError as err:
            return False
    
    def get_all_data(self):
        products = self.collection.find({})
        return products
    
    def get_by_entity(self, entity):
        products = self.collection.find({ "entity": {"$in": entity} })
        return products
    
    def get_by_entities(self, entities):
        products = self.collection.find({ "entity": {"$in": entities}})
        return products
