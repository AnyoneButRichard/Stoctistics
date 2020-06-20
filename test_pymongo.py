from pymongo import MongoClient

client = MongoClient("mongodb+srv://alexi:bkj1tUomlpAXIovl@stoctistics-vjvbe.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["test"]
collection = db[test]

test_stock = {"_id": , "stock_name": SPY, "price": 50000}

collection.insert_one({test_stock})