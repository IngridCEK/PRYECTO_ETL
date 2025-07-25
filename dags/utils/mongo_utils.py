from pymongo import MongoClient


def get_mongo_collection(uri, db_name, collection_name):
  
    client = MongoClient(uri)
    
    # acceso a mi base de datos 
    db = client[db_name]
    
    
    collection = db[collection_name]
    
    #client es la conexión activa con MongoDB
    return collection, client