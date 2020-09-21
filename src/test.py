from stocks import Stocks_Helper
from database import Data_Client

def run():
    helper = Stocks_Helper()
    helper.retrieve("MSFT")
    return helper
