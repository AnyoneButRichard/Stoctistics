import pymongo
from pymongo import MongoClient
from datetime import date

cluster = MongoClient('mongodb+srv://admin:MPyhQ9kwjo1pbUz2@cluster0-nm4ov.azure.mongodb.net/Cluster0?retryWrites=true&w=majority')

today = date.today();

# CRUD
# CREATE (POST)
# READ (GET)
# UPDATE (PUT)
# DELETE (DELETE)

# database
cluster = cluster["test"]

# collections
stocks = cluster.stocks

# Counts how many objects are in the collection
index = stocks.count_documents({})
print(index)

# NOTE YOU CAN ALSO ADD AN ID TO FIND

# PUT OPERATION
# Insert One
test_stock = {"_id": "SPY - " + str(today) + " - " + str(index), "index": index, "stock_name": "SPY", "price": 50000,
            "time_date": str(today)}
confirmationResult = stocks.insert_one(test_stock)

# If database successfully inserts database
if confirmationResult.acknowledged:
    print("successfully inserted: " + confirmationResult.inserted_id)

# Insert Many
# stocks.insert_man({post1},{post1})

# PUT operation
# stocks.update_one({
#     "index": index - 1
# }, {
#     "$set": {
#         "price": 20000
#     }
# })

# DELETE operation
# stocks.delete_one({
#     "index": index - 1
# })

# GET operation
stock = stocks.find_one({"index": index})
print(stock)