from datetime import datetime
import pandas as pd

# Personal Libraries
from regex import Regex_Helper

MORNING=" 00:00:00"
EVENING=" 23:59:00"

class Time_Helper:
    
    def Month_Day_Year(self, date):
        dt = datetime.strptime(date, "%Y/%m/%d")
        return datetime.strftime(dt, "%m/%d/%y") 

    def start(self, date):
        reg = Regex_Helper()
        if(reg.is_date(date) == True):
            date = date + MORNING        
            elem = datetime.strptime(date, "%m/%d/%y %H:%M:%S")
            timestamp = pd.Timestamp(elem.timestamp(), unit='s') 
            return timestamp
        else:
            # throw error here
            pass

    def end(self, date):
        reg = Regex_Helper()
        if(reg.is_date(date) == True):
            date = date + EVENING
            elem = datetime.strptime(date, "%m/%d/%y %H:%M:%S")
            timestamp = pd.Timestamp(elem.timestamp(), unit='s')
            return timestamp
        else:
            # throw error here
            pass 

    def now(self):
        elem = datetime.now()
        timestamp = pd.Timestamp(elem.timestamp(), unit='s')
        return timestamp 
     
