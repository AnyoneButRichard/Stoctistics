from pymongo import MongoClient
from configparser import ConfigParser

DEFAULT_PORT=27017
DB_NAME='Stoctistics'
CONFIG_FILE='/home/richard/Stoctistics/config.ini'

class Data_Client:
    def __init__(self, port=DEFAULT_PORT):
        self.port = port

    def __getitem__(self, collection):
        
        ### Get Credentials
        config = ConfigParser()
        config.read(CONFIG_FILE)
        pwd = config.get("DATABASE", "pwd")
        user = config.get("DATABASE", "user")

        ### Connect to the database        
        client = MongoClient(port=self.port)
        db = client[DB_NAME]
        db.authenticate(user, pwd) 

        ### Return the collection
        return db[collection]
