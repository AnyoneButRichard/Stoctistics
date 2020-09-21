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

class Options_Record:
    # (Class) Options_Record
    # ==================================================
    # Inputs: (str) symbol
    # Attributes:
    
    def __init(self, symbol):
        ticker = yf.Ticker(self.symbol)
        self.dates = ticker.options

    # to_dataframe
    # ==================================================
    # Inputs:
    # Outputs: (DataFrame) df
    # 
    # Function:
    # Converts a symbol to a dataframe to a tuple
    # of calls and puts
    def to_dataframe_list(self):
        df_list = {}
        df_list["dates"] = self.dates
        
        ticker = yf.Ticker(self.symbol)
        for date in dates:
            opt = ticker.option_chain(date)
            df_list["calls"][date] = opt.calls
            df_list["puts"][date] = opt.puts
            
        return df_list
        
        
          
    
