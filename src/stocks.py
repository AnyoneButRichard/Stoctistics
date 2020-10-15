import yfinance as yf
import pandas as pd
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

# Personal Modules
from database import Data_Client
from log import Log_Tool
from timer import Time_Helper 
from regex import Regex_Helper

LOG_FILENAME="/home/richard/Stoctistics/logs/stocks.log"
TICKER_FILENAME="/home/richard/Stoctistics/resources/tickers.txt"
COLLECTION_NAME="stocks"
INTERVAL="1m"
 
class Stocks_Record:  
 
    # (Class) Stocks_Record
    # ==========================================================
    # Inputs: (str) symbol
    # Attributes: 
    # (str) self.symbol, (datetime) self.timestamp, (str) self.date, 
    # (float) open, (float) close, (float) high, (float) low,
    # (int) volume, (int) dividends, (int) splits, (str) _id
    # 
    # Functions: 
    # Converts a symbol into a ticker using yfinance
    # and then generates a dictionary that can be
    # stored on the database later. Also generates
    # an _id to track down the appropriate document
    def __init__(self, symbol, period=""):
        self.period = period
        self.symbol = symbol
    
    # to_dataframe
    # =================================================
    # Inputs:
    # Outputs: (DataFrame) df
    #
    # Function:
    # Converts a symbol to a dataframe of its ticker history
    # under one of two scenarios:
    # 1) if period is empty, return the last entry (shortcut)
    # 2) if period is defined, return the entire dataframe
    def to_dataframe(self):
        ticker = yf.Ticker(self.symbol)
        if(self.period == ""):
            df = ticker.history(period="1d", interval=INTERVAL)
            return df.tail(1)
        else:
            df = ticker.history(period=self.period, interval=INTERVAL)
            return df

    # to_document
    # ===============================================
    # Inputs:
    # Outputs: (list) doc_list
    # 
    # Function:
    # Generates a document using the class attributes
    # that were stored upon initialization and appends
    # to a list for each timestamp generated
    def to_document(self):
        doc_list = []
        df = self.to_dataframe()
        
        for timestamp in df.index:
            doc = {}
            doc["Timestamp"] = timestamp
            doc["Open"] = df["Open"][timestamp]
            doc["Close"] = df["Close"][timestamp]
            doc["High"] = df["High"][timestamp]
            doc["Low"] = df["Low"][timestamp]
            doc["Volume"] = int(df["Volume"][timestamp])
            doc["Dividends"] = int(df["Dividends"][timestamp])
            doc["Splits"] = int(df["Stock Splits"][timestamp])
            doc_list.append(doc) 
        
        return doc_list

#########################################################
#########################################################
class Stocks_Helper:

    # (Class) Stocks_Helper
    # ===============================================
    # Inputs: (str or list) user_input
    # Attributes:
    # (list) symbols
    #
    # Function:
    # Grabs initial user input which is either a list of tickers or
    # a file that has a list of tickers. If the latter, convert to
    # list of tickers. Helper that can either generate entries and put
    # them on the database, or retrieve entries in the format of a
    # DataFrame. Retrievals and updates will be logged

    ### Class instances
    columns = ["Open","Close","High","Low","Volume","Dividends","Splits"]
    periods = ("","1d","7d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max")

    def __init__(self, user_input=TICKER_FILENAME, period=""):

        ### Object instances
        self.symbols = []
        self.period = ""

        ### Parsing user input
        if isinstance(user_input, str):
            with open(user_input) as inFile:
                self.symbols = inFile.read().splitlines()
        elif user_input != "":
            self.symbols = user_input
    
        ### Parsing period
        if period in self.periods:
            self.period = period
 
    # store
    # =======================================================
    # Inputs: (str) symbol
    # Outputs: 
    #
    # Function: Generates a Stocks_Record object that
    # helps translate information to a historical
    # subdocument. Then generates queries that can
    # locate the correct document to append the
    # subdocument to.
    def store(self, symbol):

        ### Start Timer
        #store_timer = Log_Tool(LOG_FILENAME)
        #store_timer.start("stocks.store")

        ### Retrieve Collection
        client = Data_Client()
        collection = client[COLLECTION_NAME]
        
        ### Establish a record
        record = Stocks_Record(symbol, self.period)
        doc_list = record.to_document()

        for doc in doc_list:
            date = doc["Timestamp"].strftime("%m/%d/%y")
            _id = symbol + " - " + date
        
            ### May not be required at all
            ### Remove existing entry if found
            # collection.update_one(
            #   { #Find document query
            #    "_id": _id
            #   },
            #   { #Update document query
            #    "$pull": {"history": doc}
            #   } 
            #)

            ### Pushing entry onto existing document's array
            collection.update_one(
                { #Find document query
                 "_id": _id
                },
                { #Update document query
                 "$push": {"history": doc},
                 "$setOnInsert": {"_id": _id, "Date": date, "Symbol": symbol}
                },
                #Options
                upsert=True
            )

        ### End Timer
        #store_timer.end("stocks.store")
     
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
        update_timer.start("stocks.update")

        ### Multithreading through symbols list
        with ThreadPool(threads) as pool:
            pool.map(self.store, self.symbols)
        
        ### End Timer
        update_timer.end("stocks.update")


    # retrieve
    # ========================================================
    # Inputs: (str) symbol, (str) start date, (str) end date
    # Outputs: (DataFrame) df
    #
    # Function:
    # Retrieves dataframe history for 1 of 3 possibilities:
    # 1) Entire dataframe history (no inputs)
    # 2) Entire dataframe history starting from start date til today
    # 3) Entire dataframe history from start date to end date

    def retrieve(self, symbol, start_date="", end_date=""):
        
        ### Start Timer
        retrieve_timer = Log_Tool(LOG_FILENAME)
        retrieve_timer.start("stocks.retrieve")
        
        ### Retrieve Collection
        client = Data_Client()
        collection = client[COLLECTION_NAME]

        ### Create Helpers
        time = Time_Helper()

        ### Situation 1: No inputs, from start to end
        if(start_date == ""):
            query = {"Symbol": symbol}

        ### Situation 2: One start date input: 
        elif(end_date == ""):
            start_date = time.start(start_date) 
            query = {"Symbol": symbol, "history.0.Timestamp": {"$gte": start_date}}
    
        ### Situation 3:
        else:
            start_date = time.start(start_date)
            end_date = time.end(end_date)
            query = {"Symbol": symbol, "history.0.Timestamp": {"$gte": start_date, "$lte": end_date}}

        ### Retrieve list and convert to dataframe_list
        doc_list = collection.find(query) 
        df = pd.DataFrame(columns = self.columns)
        
        ### Convert and append each entry to the dataframe
        for doc in doc_list:
            doc_df = pd.DataFrame(doc["history"])
            df = df.append(doc_df.set_index("Timestamp"))
        
        ### Sort and return the dataframe
        df = df.sort_index()
        return df

        ### NOTE if in the future you want to be able to select time ranges, you should either do it within the dataframe,
        ### or within the for loop appending each entry to the dataframe
            
        

