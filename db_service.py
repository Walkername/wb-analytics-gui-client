import pymongo

def get_all_data(url, db_name, col_name):
    # MongoDB Connection (replace with your MongoDB URI and database/collection)
    client = pymongo.MongoClient(url)
    db = client[db_name]
    collection = db[col_name]

    # Fetch all products (adjust query if needed to filter products)
    products = collection.find({})
    
    return products

def get_by_entity(url, db_name, col_name, entity):
    # MongoDB Connection (replace with your MongoDB URI and database/collection)
    client = pymongo.MongoClient(url)
    db = client[db_name]
    collection = db[col_name]

    # Fetch products by entity
    products = collection.find({ "entity": {"$in": ["Куртки", "Свитеры"]}})
    
    return products

def get_by_entities(url, db_name, col_name, entities):
    # MongoDB Connection (replace with your MongoDB URI and database/collection)
    client = pymongo.MongoClient(url)
    db = client[db_name]
    collection = db[col_name]

    # Fetch products by entities
    products = collection.find({ "entity": {"$in": entities}})
    
    return products