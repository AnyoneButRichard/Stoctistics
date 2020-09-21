import json
import data
import logging
from datetime import datetime
import yfinance as yf
from pymongo import MongoClient

CRED_FILENAME = '/home/richard/Stoctistics/resources/cred.json'
TICKER_FILENAME = '/home/richard/Stoctistics/resources/tickers.txt'

# cluster_connect:
# ==============================================
# Inputs: (str) dbname = "astocks"
# Outputs: (obj) cluster
#
# Function: Connects to the database cluster and returns the cluster as an object
# by loading the credentials file (private) and then invoking the MongoClient()
# method from the pymongo library
def cluster_connect(dbname = "astocks"):
    with open(CRED_FILENAME) as inFile:
        cred = json.load(inFile)

    connection = "mongodb://" + cred["user"] + ":" + cred["password"] + "@stoctistics-shard-00-00-vjbe.azure.mongodb.net:27017,stoctistics-shard-00-01-vjbe.azure.mongodb.net:27017,stoctistics-shard-00-02-vjvbe.azure.mongodb.net:27017/" + dbname + "?ssl=true&replicaSet=Stoctistics-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(connection)
    return client

# start_logger:
# =======================================================
# Inputs: (obj) logger
# Outputs: (datetime) start
# 
# Function:
# Inline function that records start time to logs and
# returns to the user the 'start' time
def start_logger(logger):
    start = datetime.now()
    now = start.strftime("%m/%d/%y (%H:%M:%S)")
    logger.info('Start Time: ' + now)
    return start

# end_logger:
# =======================================================
# Inputs: (datetime) start, (obj) logger
# Outputs: None
#
# Function:
# Inline function that records end time to logs
# and logs the total elapsed time as well
def end_logger(start, logger):
    end = datetime.now()
    now = end.strftime("%m/%d/%y (%H:%M:%S)")
    logger.info('End Time: ' + now)
    total_time = str(round((end - start).total_seconds(), 3))
    logger.info('Elapsed Time: ' + total_time + ' seconds')

# partition:
# ==============================================
# Inputs: (list) ls, (int) divs
# Outputs: (generator) symbol
#
# Function: Generates a partitioned list based on the
# number of divisions requested. Will come out in the
# form of a "list of lists"
def partition(ls, divs):
    for i in range(0, len(ls), divs):
        yield ls[i:1 + divs]


# Move to rstocks when revised necessary
# generate_rcollections:
# ================================================================
# Inputs: (str) filename = "tickers.txt"
# Outputs: None
#
# Function: Runs through list of tickers in the tickers.txt, and generates
# an empty collection inside of the "rstocks" database for each ticker.
def generate_rcollections(filename=TICKER_FILENAME):
    with open(filename) as inFile:
        tickers = inFile.read().splitlines()
    cluster = cluster_connect()
    db = cluster["rstocks"]
    for ticker in tickers:
        db.createCollection(ticker)
