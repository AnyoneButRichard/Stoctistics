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
        record_timer = Log_Tool(ERROR_FILENAME)
        ticker = yf.Ticker(symbol)
        self.symbol = symbol

        # catch here in case there is no options available for stock
        try:
            self.expiries = [time.Month_Day_Year(expiry) for expiry in ticker.options] 
            self.strikes = list(ticker.option_chain(ticker.options[0]).calls.strike)
        except IndexError:
            print("Skipping: ", symbol)
            record_timer.error("options_record.init " + symbol)
        

    # to_list_by_expiry
    # ==================================================
    # Inputs:
    # Outputs: (list) list_by_expiry
    # 
    # Function:
    # Goes through and traverses call/put options by expiry.
    # Then runs "to_list_by_strike" which will spit out all the
    # documents at all strike points for that expiry, before
    # extending each document onto the main list_by_expiry
    def to_list_by_expiry(self):
        time = Time_Helper() 
        self.timestamp = time.now() 
        self.date = self.timestamp.strftime("%m/%d/%y")
        list_by_expiry = []
        ticker = yf.Ticker(self.symbol)
        expiries = ticker.options  

        for expiry in expiries:
            opt = ticker.option_chain(expiry)
            list_by_expiry.extend(self.to_list_by_strike(opt.calls, "Call", expiry))
            list_by_expiry.extend(self.to_list_by_strike(opt.puts, "Put", expiry))      

        return list_by_expiry
        
    # to_list_by_strike
    # ==================================================
    # Inputs: (Dataframe) df, (string) contract, string (expiry)
    # Outputs: (list) list_by_strike
    #
    # Function:
    # This grabs either a call or a put dataframe, and converts
    # all of the strike/expiry price points into a document
    def to_list_by_strike(self, df, contract, expiry):
        time = Time_Helper()
        list_by_strike = []
        for index in df.index:
            doc = {} 
            doc["Contract"] = contract
            doc["Expiry"] = time.Month_Day_Year(expiry)
            doc["Strike"] = str(df["strike"][index])
            doc["Data"] = {}
            doc["Data"]["Timestamp"] = self.timestamp
            doc["Data"]["Bid"] = df["bid"][index]
            doc["Data"]["Ask"] = df["ask"][index]
            doc["Data"]["Last Price"] = df["lastPrice"][index]
            doc["Data"]["Last Trade"] = df["lastTradeDate"][index]
            doc["Data"]["Change"] = round(df["change"][index], 2)
            doc["Data"]["Percent Change"] = round(df["percentChange"][index], 2)
            doc["Data"]["Volume"] = float(df["volume"][index])
            doc["Data"]["Open Interest"] = float(df["openInterest"][index])
            doc["Data"]["Implied Volatility"] = df["impliedVolatility"][index]
            doc["Data"]["In The Money"] = bool(df["inTheMoney"][index])
            doc["Data"]["Contract Size"] = df["contractSize"][index]
            doc["Data"]["Currency"] = df["currency"][index]
            list_by_strike.append(doc)
        return list_by_strike
                          

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
        doc_list = record.to_list_by_expiry()

        for doc in doc_list:            
            date = record.date
            contract = doc["Contract"]
            _id = symbol + " - " + contract + " - " + date

            ### May not be required at all
            ### Remove existing entry if found
            #collection.update_one(
            #    { #Find document query
            #     "_id": _id
            #    },
            #    { #Update document query
            #     "$pull": {"history": 
            #                {doc["Expiry"]: 
            #                    {doc["Strike"]: doc["Data"]}
            #                }
            #              }
            #    },
            #)

            ### Pushing existing entry if found
            collection.update_one(
                { #Find document query
                 "_id": _id
                },
                { #Update document query
                 "$push": {"history":
                            {doc["Expiry"]:
                                {doc["Strike"]: doc["Data"]}
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

