import json
import data
import scrape
import logging
from datetime import datetime
import yfinance as yf
from pymongo import MongoClient

# cluster_connect:
# ==============================================
# Inputs: (str) dbname = "astocks"
# Outputs: our stocks database cluster
#
# Function: Connects to the database cluster and returns the cluster as an object
# by loading the credentials file (private) and then invoking the MongoClient()
# method from the pymongo library
def cluster_connect(dbname = "astocks"):
    with open('../resources/cred.json') as inFile:
        cred = json.load(inFile)

    connection = "mongodb://" + cred["user"] + ":" + cred["password"] + "@stoctistics-shard-00-00-vjbe.azure.mongodb.net:27017,stoctistics-shard-00-01-vjbe.azure.mongodb.net:27017,stoctistics-shard-00-02-vjvbe.azure.mongodb.net:27017/" + dbname + "?ssl=true&replicaSet=Stoctistics-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(connection)
    return client

# generate_rcollections:
# ================================================================
# Inputs: (str) filename = "tickers.txt"
# Outputs: None
#
# Function: Runs through list of tickers in the tickers.txt, and generates
# an empty collection inside of the "rstocks" database for each ticker.
def generate_rcollections(filename = "../resources/tickers.txt"):
    with open(filename) as inFile:
        tickers = inFile.read().splitlines()
    cluster = cluster_connect()
    db = cluster["rstocks"]
    for ticker in tickers:
        db.createCollection(ticker)

# auto_astocks:
# =================================================================
# Inputs: (str) filename = "tickers.txt"
# Outputs: None
#
# Function:
# Automatically generates documents for each symbol listed in tickers.txt
# A debug log is generated due to the yfinance library having conflicts with
# various tickers, so we choose to record the error just in case.
def auto_astocks(filename = "../resources/tickers.txt"):
    now = datetime.now().strftime("%m/%d/%y (%H:%M:%S)")
    logging.basicConfig(filename='../logs/error.log', filemode ='a', level=logging.DEBUG)
    logging.info('Auto_Astocks Start Timestamp: ' + now)
    with open(filename) as inFile:
        symbols = inFile.read().splitlines()
    cluster = cluster_connect()
    db = cluster["astocks"]
    collection = db["stocks"]

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            add_data_astocks(collection, ticker, "60d", "5m")
        except IndexError:
            logging.error('Cannot find ' + symbol)
   
# adds data to a collection in the form of astocks json
def add_data_astocks(collection, ticker, per = "60d", inc = "5m"):
    json_list = scrape.serialize_astocks(ticker, period = per, interval = inc)
    for json_data in json_list:
        json_id = json_data["_id"]
        collection.update_one({"_id":json_data["_id"]}, {"$set" :json_data}, upsert=True)

# adds data to a collection in the form of rstocks json (refer to readme)
# format this into the new method for serializing (incomplete)
def add_data_rstocks(collection, ticker, per = "60d", inc = "5m"):
    df = ticker.history(period = per, interval = inc)
    for timestamp in df.index:
        json_data = scrape.serialize_rstocks(df, timestamp)
        collection.update_one({"_id": i}, {"$setOnInsert" :json_data}, upsert=True)

# incomplete
def get_daily_rstocks(db):
    for i in db.collection_names():
        ticker = db[i].name


