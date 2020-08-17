### Libraries
import json
import time
import logging
import yfinance as yf
from datetime import datetime
from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadPool

# User Defined
import data

LOG_FILENAME="/home/richard/Stoctistics/logs/options.log"
TICKER_FILENAME="/home/richard/Stoctistics/resources/tickers.txt"

# create_doc:
# ===============================================================
# Inputs: (str) symbol, (str) date
# Outputs: (dict) doc
#
# Function:
# Inline function that generates an empty doc of an 
# options format.
def create_doc(symbol, date):
    doc = {}
    doc["_id"] = symbol + " - " + date
    doc["Symbol"] = symbol
    doc["Date"] = date
    doc["Time"] = {}        # list-like
    doc["Timestamp"] = {}   # list-like
    doc["Strikes"] = {}     # list-like 
    doc["Expiries"] = {}    # list-like

    doc["Calls"] = {}       # nested map doc["Calls"]["Expiry"]["Strike"]
    doc["Puts"] = {}        # nested map doc["Puts"]["Expiry"]["Strike"]

def create_option(exp):
    option = {}

def serialize_option(symbol):
    try:
        ticker = yf.Ticker(symbol)
        exp_list = ticker.options

        for exp in exp_list:
            opts = ticker.option_chain(exp)
            calls = opts.calls
            puts = opts.puts    
			strike_list = [strikes for strikes in calls["strike"]]

            date = df.index[0].strftime("%m/%d/%y")
            doc = create_doc(symbol, date)
			
			for strike in strike_list:

