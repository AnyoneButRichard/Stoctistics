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
TICKER_FILENAME="/home/richard/Stoctistics/resources/tickers.txt"
COLLECTION_NAME="options"
INTERVAL="1m"

class Options_Record:
    # (Class) Options_Record
    # ==================================================
    # Inputs: (str) symbol
    # Attributes:
    
    def __init(self, symbol):
        time = Time_Helper()
        ticker = yf.Ticker(symbol)
        self.symbol = symbol
        self.dates = [time.Month_Day_Year(date) for date in ticker.options]
        self.strikes = list(ticker.option_chain(self.dates[0]).calls.strike)

    # to_dataframe
    # ==================================================
    # Inputs:
    # Outputs: (DataFrame) df
    # 
    # Function:
    # Converts a symbol to a dataframe to a tuple
    # of calls and puts
    def to_dictionary(self):
        time = Time_Helper()
        order = {}
        order["Timestamp"] = time.now() 
        ticker = yf.Ticker(self.symbol)
        dates = ticker.options  
        for date in dates:
            opt = ticker.option_chain(date)
            order["Calls"] = opt.calls
            puts = opt.puts
            
        return df_list
        
    # to_document
    # ==================================================
    # Inputs:
    # Outputs: (list) doc_list
    #
    # Function:
    # Converts a dict into a proper document that is
    # prepared to be inserted into the database
    def to_document(self):
        doc_list = []
        
        for date in self.dates:
            for strike in self.strikes:
                doc = {}
                doc["Timestamp"] = timestamp
                doc["Contract"] = 
                doc["Expiry"] = strike
                doc["Date"] = date
                
                
                 

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
        store_timer.start("options.store")

        ### Retrieve Collection
        client = Data_Client()
        collection = client[COLLECTION_NAME]

        ### Establish a record
        record = Options_Record(symbol)
        doc_list = record.to_document()

        for doc in doc_list:
            date = doc["Timestamp"].strftime("%m/%d/%y")
            contract = doc["Contract"]
            _id = symbol + " - " + contract + " - " + date

            ### Remove existing entry if found
            collection.update_one(
                { #Find document query
                 "_id": _id
                },
                { #Update document query
                 "$pull": {"history": 
                            {doc["Expiry"]: 
                                {doc["Strike"]: doc["history"]}
                            }
                          }
                },
            )

            ### Pushing existing entry if found
            collection.update_one(
                { #Find document query
                 "_id": _id
                },
                { #Update document query
                 "$push": {"history":
                            {doc["Expiry"]:
                                {doc["Strike"]: doc["history"]}
                            }
                          },
                 "$setOnInsert": {"_id": _id, "Date": date, "Symbol": symbol,
                 "Contract": contract}
                },
                #Options
                upsert=True
            )

        ### End Timer
        store_timer.end("options.store") 
