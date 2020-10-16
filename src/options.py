### Standard Libraries
from datetime import datetime

### Third Party Libraries
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import yfinance as yf

### Personal Libaries
from database import Data_Client
from log import Log_Tool
from timer import Time_Helper 
from regex import Regex_Helper # maybe rename to Parser

LOG_FILENAME="/home/richard/Stoctistics/logs/options.log"
ERROR_FILENAME="/home/richard/Stoctistics/logs/err_options.log"
TICKER_FILENAME="/home/richard/Stoctistics/resources/tickers.txt"
COLLECTION_NAME="options"
INTERVAL="1m"

class Options_Record:
    # (Class) Options_Record
    # ==================================================
    # Inputs: (str) symbol
    # Attributes:
    
    def __init__(self, symbol):

        time = Time_Helper()
        self.ticker = yf.Ticker(symbol)
        self.symbol = symbol

        # catch here in case there is no options available for stock
        try:
            self.expiries = [time.Month_Day_Year(expiry) for expiry in self.ticker.options] 
            self.strikes = list(self.ticker.option_chain(self.ticker.options[0]).calls.strike)
        except IndexError:
            print("Skipping: ", symbol)

    # store
    # ==================================================
    def store(self, collection):
        time = Time_Helper()
        self.timestamp = time.now()
        self.date = self.timestamp.strftime("%m/%d/%y")


        ### 

        ### Update the individual ticker data        
        for expiry in self.ticker.options:
            opt = self.ticker.option_chain(expiry)
            calls = opt.calls
            puts = opt.puts
        
            for index in calls.index:
                self.contract = "Call"
                self.expiry = time.Month_Day_Year(expiry)
                self.strike = str(calls["strike"][index])
                _id = self.symbol + " - " + self.date + " - " + self.contract
                h_query = "history." + self.expiry + "." + self.strike
                collection.update(
                    {
                     "_id": _id
                    },
                    {
                     "$push": {h_query: 
                                self.to_document(calls, index) 
                              }, 
                     "$setOnInsert": {"_id": _id, "Date": self.date, "Symbol": self.symbol,
                     "Contract": self.contract} 
                    },
                    upsert=True
                )

            for index in puts.index:
                self.contract = "Put"
                self.expiry = time.Month_Day_Year(expiry)
                self.strike = str(puts["strike"][index])
                _id = self.symbol + " - " + self.date + " - " + self.contract
                h_query = "history." + self.expiry + "." + self.strike
                collection.update(
                    {
                     "_id": _id
                    },
                    {
                     "$push": {h_query:
                                  self.to_document(puts, index)
                              }, 
                     "$setOnInsert": {"_id": _id, "Date": self.date, "Symbol": self.symbol,
                     "Contract": self.contract} 
                    },
                    upsert=True
                )  


    # to_document
    # ==================================================
    def to_document(self, df, index):
        doc = {}
        doc["Timestamp"] = self.timestamp
        doc["Bid"] = df["bid"][index]
        doc["Ask"] = df["ask"][index]
        doc["Last Price"] = df["lastPrice"][index]
        doc["Last Trade"] = df["lastTradeDate"][index]
        doc["Change"] = round(df["change"][index], 3)
        doc["Percent Change"] = round(df["percentChange"][index], 3)
        doc["Volume"] = float(df["volume"][index])
        doc["Open Interest"] = float(df["openInterest"][index])
        doc["Implied Volatility"] = round(df["impliedVolatility"][index], 3)
        doc["In The Money"] = bool(df["inTheMoney"][index])
        doc["Contract Size"] = df["contractSize"][index]
        doc["Currency"] = df["currency"][index]
        return doc
                                 
##########################################################
##########################################################
class Options_Helper:

    # (Class) Options_Helper
    # ============================================================
    # Inputs: (str or list) user_input
    # Attributes:
    # (list) symbols
    #
    # Function:
    # Grabs initial user input which is either a list of tickers
    # or a file that has a list of tickers. If the latter, convert
    # to a list of tickers. Helper can either generate entries and
    # put them on the database, or retrieve entries in the format of
    # a DataFrame. Retrievals and updates will be logged
        
    ### Class instances 
    columns = ["Bid", "Ask", "Last Price", "Last Trade", "Change", "Percent Change", "Volume", "Open Interest", "Implied Volatility", "In The Money", "Contract Size", "Currency"]

    def __init__(self, user_input=TICKER_FILENAME, period=""):

        ### Object instances
        self.symbols = []

        ### Retrieve Collection
        self.client = Data_Client()
        self.collection = self.client[COLLECTION_NAME]

        ### Parsing user input
        if isinstance(user_input, str):
            with open(user_input) as inFile:
                self.symbols = inFile.read().splitlines()
        elif user_input != "":
            self.symbols = user_input

    # store
    # ===============================================================
    # Inputs: (str) symbol
    # Outputs:
    #
    # Function: Generates an Options_Record object that helps
    # translate information to a historical subdocument. Then
    # Generates queries that can locate the correct document
    # to append the subdocument to.
    def store(self, symbol):
        
        ### Start Timer
        store_timer = Log_Tool(LOG_FILENAME)
        store_timer.start("options.store " + symbol)

        ### Establish a record
        record = Options_Record(symbol)
        record.store(self.collection)

        ### End Timer
        store_timer.end("options.store " + symbol) 

    # update 
    # =======================================================
    # Inputs:
    # Outputs: 
    # 
    # Function:
    # Cycles through the symbols list and runs "store" on each
    # of the symbols with multithreads
    def update(self, threads=12):
    
        ### Start Timer
        update_timer = Log_Tool(LOG_FILENAME)
        update_timer.start("options.update")

        ### Multithreading through symbols list
        with ThreadPool(threads) as pool:
            pool.map(self.store, self.symbols)
        
        ### End Timer
        update_timer.end("options.update")

