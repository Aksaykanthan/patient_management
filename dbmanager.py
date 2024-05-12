from typing import List
import pymongo



class DBManager:

    def __init__(self) -> None:
        dbname = "Medilink"
        collections = ["doctors","patients","medicines"]
        self.dbname = dbname
        self.myclient = pymongo.MongoClient("mongodb://0.0.0.0:27017/")
        self.db = self.myclient[dbname]
        self.collections = collections
        self.init()
    
    
    def init(self):
        dblist  = self.myclient.list_database_names()
        if self.dbname in dblist:
            print("The database exists.")
            return
        print(f"The database {self.dbname} created.")
        
        aval_collection = self.db.list_collection_names()
        for collection in self.collections:
            if collection not in aval_collection:
                mycol = self.db[collection]
                print(f"Collection {collection} created.")
    



