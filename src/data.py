import json
import data
from pymongo import MongoClient

def cluster_connect(dbname = "rstocks"):
    with open('../resources/cred.json') as inFile:
        cred = json.load(inFile)

    connection = "mongodb://" + cred["user"] + ":" + cred["password"] + "@stoctistics-shard-00-00-vjbe.azure.mongodb.net:27017,stoctistics-shard-00-01-vjbe.azure.mongodb.net:27017,stoctistics-shard-00-02-vjvbe.azure.mongodb.net:27017/" + dbname + "?ssl=true&replicaSet=Stoctistics-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(connection)
    return client


def add_rcollections(db, filename = "../resources/tickers.txt"):
    with open(filename) as inFile:
        tickers = inFile.read().splitlines()
    cluster = connect()
    db = cluster["rstocks"]
    for i in tickers:
        db.createCollection(i)

def add_data_astocks(collection, ticker, per = "60d", inc = "5m"):
    symbol = ticker.info.symbol

# adds data to a collection in the form of json2 (refer to readme)
def add_data_rstocks(collection, ticker, per = "60d", inc = "5m"):
    df = ticker.history(period = per, interval = inc)
    for i in df.index:
        status = collection.find_one({"_id": i})
        if(status == None):
            json_data = data.serialize_dataframe_rstocks(df, i)
            collection.insert_one(json_data) 

        # alternative (needs testing)
        # json_data = data.serialize_dataframe_rstocks(df, i)
        # collection.update({"_id": i}, {$setOnInsert :json_data}, {upsert: True})

def get_daily_rstocks(db):
    for i in db.collection_names():
        ticker = db[i].name
        data = getHistory(ticker, per = "1d")
        addData2(db[i], data)




