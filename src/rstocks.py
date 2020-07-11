# Libraries
import json
import time
import logging
import yfinance as yf
from datetime import datetime
from pymongo import MongoClient
from multiprocessing import Pool as ThreadPool

# User defined
import data

LOG_FILENAME = "../logs/rstocks.log"
TICKER_FILENAME = "../resources/tickers.txt"

# create_doc:
# ========================================================
# Inputs: (str) symbol, (str) date
# Outputs: (dict) doc
#
# Function:
# Inline function that generates an empty doc. Very useful
# because we don't need to generate an array of dicts or
# make a deep copy of a dict which can become expensive
def create_doc(symbol, date):
    doc = {}
    doc["_id"] = date
    doc["Date"] = date
    doc["Symbol"] = symbol 
    doc["Time"] = []
    doc["Timestamp"] = []
    doc["Open"] = []
    doc["Close"] = []
    doc["High"] = []
    doc["Low"] = []
    doc["Volume"] = []
    doc["Dividends"] = []
    doc["Stock Splits"] = []
    return doc

# serialize_stock
# ==============================================================
# Inputs: (str) symbol, (str) period = "1d", (str) interval = "5m"
# Outputs: (list) doc_list
#
# Function:
# Given a symbol, will generate a list of historical entries
# for a stock and append stock values for each day. Once the
# dataframe entry moves to the next day, we append that
# document onto the list and generate a brand new day document.
# At the end, we return the list of documents for given stock.
def serialize_stock(symbol, period = "1d", interval = "5m"):
   
    # Start Timer
    logging.basicConfig(filename=LOG_FILENAME, filemode="a", level=logging.INFO)
    logger = logging.getLogger("rstocks.serialize_stock")
    start = data.start_logger(logger)
    
    # Initialize and generate data
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period = period, interval = interval)
        date = df.index[0].strftime("%m/%d/%y")
        doc = create_doc(symbol, date)
        doc_list = []
    except IndexError:
        logger.error("rstocks.serialize_stock: Ticker symbol [" + symbol + "] was not found!") 

    for i in df.index:
        timestamp = i
        newdate = timestamp.strftime("%m/%d/%y")

        # new date finalizes current document and generates a new document
        if(newdate != date):
            date = newdate
            doc_list.append(doc)
            doc = create_doc(symbol, date)
       
        # append data to the document 
        doc["Time"].append(timestamp.strftime("%H:%M:%S"))
        doc["Timestamp"].append(timestamp)
        doc["Open"].append(df["Open"][i])
        doc["Close"].append(df["Close"][i])
        doc["High"].append(df["High"][i])
        doc["Low"].append(df["Low"][i])
        doc["Volume"].append(int(df["Volume"][i]))
        doc["Dividends"].append(int(df["Dividends"][i]))
        doc["Stock Splits"].append(int(df["Dividends"][i]))

    doc_list.append(doc)
    
    # End Timer
    data.end_logger(start, logger)
    
    return doc_list
    
# store_stock:
# ====================================================================
# Inputs: (str) symbol, (str) period = "1d", (str) interval = "5m"
# Outputs: None
#
# Function:
# Makes a connection to the astock database, stocks collection.
# Generates stock history information for the symbol provided
# and serializes it into the "astock" format. Then goes through
# and updates the document if found in the collection, or generates
# a brand new one if not found.
def store_stock(symbol, period = "1d", interval = "5m"):

    # Start Timer
    logging.basicConfig(filename=LOG_FILENAME, filemode="a", level=logging.INFO)
    logger = logging.getLogger("rstocks.store_stock")
    start = data.start_logger(logger)

    # Retrieve collection
    cluster = data.cluster_connect()
    db = cluster["rstocks"]
    coll = db[symbol]

    # Update document if found, generate new doc if not found
    doc_list = serialize_stock(symbol, period = period, interval = interval)
    for doc in doc_list:
        coll.update_one({"_id": doc["_id"]}, {"$set" :doc}, upsert=True)

    # End Timer
    data.end_logger(start, logger)
    logger.debug('Ticker symbol stored: ' + symbol)

# update_stocks:
# ====================================================================
# Inputs: (str) filename = "tickers.txt", (int) threads = 16
# Outputs: None
#
# Function:
# Automatically generates documents for the rstock
# database for each symbol listed in tickers.txt
# A debug log is generated due to the yfinance library
# having conflicts with various tickers, we choose
# to record the error just in case. View 'logs/rstocks_error.log'
# for more info on errors
def update_stocks(filename=TICKER_FILENAME, threads=16):

    # Start Timer
    logging.basicConfig(filename=LOG_FILENAME, filemode="a", level=logging.INFO)
    logger = logging.getLogger("rstocks.update_stocks")
    start = data.start_logger(logger)
    
    # Generate a list of tickers
    with open(filename) as inFile:
        symbols = inFile.read().splitlines()
    
    # Use a Thread Pool to asynchronously make updates to the database
    with ThreadPool(threads) as pool:
        pool.map(store_stock, symbols)

    # End Timer
    data.end_logger(start, logger)
