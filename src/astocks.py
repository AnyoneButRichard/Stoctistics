### Libraries
import json
import time
import logging
import yfinance as yf
from datetime import datetime
from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadPool

### User Defined
import data

LOG_FILENAME="/home/richard/Stoctistics/logs/astocks.log"
TICKER_FILENAME="/home/richard/Stoctistics/resources/tickers.txt"

# create_doc:
# ===============================================================
# Inputs: (str) symbol, (str) date
# Outputs: (dict) doc
#
# Function:
# Inline function that generates an empty doc. Very useful
# because we don't need to generate an array of dicts or
# make a deep copy of a dict which can become expensive
def create_doc(symbol, date):
    doc = {}
    doc["_id"] = symbol + " - " + date
    doc["Symbol"] = symbol
    doc["Date"] = date
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

# columns_stock
# ==============================================================
# Inputs:
# Outputs: (list) columns
#
# Function:
# Returns a list of stock serialization column names
def columns_stock():
	return ["Open", "Close", "High", "Low", "Volume", "Dividends", "Stock Splits"]

# serialize_stock
# ==============================================================
# Inputs: (str) symbol, (str) period = "60d", (str) interval = "5m"
# Outputs: (list) doc_list
#
# Function:
# Given a symbol, will generate a list of historical entries
# for a stock and append stock values for each day. Once the
# dataframe entry moves to the next day, we append that 
# document onto the list and generate a brand new day document.
# At the end, we return the list of documents for given stock
def serialize_stock(symbol, period = "1d", interval = "5m"):

    ### Start Timer (removing)
    # logging.basicConfig(filename=LOG_FILENAME, filemode ="a", level=logging.INFO)
    # logger = logging.getLogger("astocks.serialize_stock")
    # start = data.start_logger(logger)

    ### Initialize and generate data
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period = period, interval = interval)
        date = df.index[0].strftime("%m/%d/%y")
        doc = create_doc(symbol, date)
        doc_list = []
    except IndexError:
        logger.error("astocks.serialize_stock: Ticker symbol [" + symbol + "] was not found!")

    for i in df.index:
        timestamp = i
        newdate = timestamp.strftime("%m/%d/%y")

        ### New date finalizes current document and generates a new document
        if(newdate != date):
            date = newdate
            doc_list.append(doc)
            doc = create_doc(symbol, date)

        ### Append data to the document
        doc["Time"].append(timestamp.strftime("%H:%M:%S"))
        doc["Timestamp"].append(timestamp)
        doc["Open"].append(df["Open"][i])
        doc["Close"].append(df["Close"][i])
        doc["High"].append(df["High"][i])
        doc["Low"].append(df["Low"][i])
        doc["Volume"].append(int(df["Volume"][i]))
        doc["Dividends"].append(int(df["Dividends"][i]))
        doc["Stock Splits"].append(int(df["Stock Splits"][i]))

    ### Add last doc to the list
    doc_list.append(doc)

    ### End Timer (removing)
    # data.end_logger(start, logger)
    
    return doc_list

# store_stock:
# ================================================================
# Inputs: (str) symbol, (str) period = "1d", (str) interval = "5m"
# Outputs: None
#
# Function:
# Makes a connection to the astock database, stocks collection.
# Generates stock history information for the symbol provided
# and serializes it into the "astock" format. Then goes through
# and updates the document if found in the collection, or generates
# a brand new one if not found.
def store_stock(symbol, period="1d", interval="5m"):

    ### Start Timer
    logging.basicConfig(filename=LOG_FILENAME, filemode="a", level=logging.INFO)
    logger = logging.getLogger("astocks.store_stock")
    start = data.start_logger(logger)

    ### Retrieve collection (threadsafe if not sharing collections)
    cluster = data.cluster_connect()
    db = cluster["astocks"]
    coll = db["stocks"]

    ### update document if found, generate new if not found
    doc_list = serialize_stock(symbol, period = period, interval = interval)

    for doc in doc_list:
        coll.update_one({"_id": doc["_id"]}, {"$set" :doc}, upsert=True)

    ### End Timer
    data.end_logger(start, logger)

# update_stocks:
# =================================================================
# Inputs: (str) filename = "tickers.txt", (int) threads = 16
# Outputs: None
#
# Function:
# Automatically generates documents for the astock
# database for each symbol listed in tickers.txt
# A debug log is generated due to the yfinance library
# having conflicts with various tickers, we choose
# to record the error just in case. View 'logs/astocks_error.log'
# for more info on errors
def update_stocks(filename=TICKER_FILENAME, threads=16):

    ### Start Timer
    logging.basicConfig(filename=LOG_FILENAME, filemode ="a", level=logging.INFO)
    logger = logging.getLogger("astocks.update_stocks")
    start = data.start_logger(logger)

    ### Generate a list of tickers
    with open(filename) as inFile:
        symbols = inFile.read().splitlines()

    ### Use a Thread Pool to asynchronously make updates to the database
    with ThreadPool(threads) as pool:
        pool.map(store_stock, symbols)
    
    ### End Timer
    data.end_logger(start, logger)

# retrieve_stock:
# ===============================================
# Inputs: (str) symbol
# Outputs: (obj) df
# 
# Function: Goes into database, retrieves all stock data for the 
# ticker symbol, and formats it into a dataframe before
# returning it (ideally matching the format of yfinance as closely as possible)
def retrieve_stock(symbol):

    ### Start Timer
	logging.basicConfig(filename=LOG_FILENAME, filemode ="a", level=logging.INFO)
	logger = logging.getLogger("astocks.retrieve_stock")
	start = data.start_logger(logger)

	# Generate search query
	query = {"Symbol": symbol}
	
	# Connect to collection
	cluster = data.cluster_connect()
	db = cluster["astocks"]
	coll = db["stocks"]

	doc_list = coll.find(query)
