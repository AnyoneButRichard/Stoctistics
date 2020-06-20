import yfinance as yf
import time
import json

def count_time(time1):
    print(round(time.time() - time1, 3), "seconds")

timer = time.time()
stock = yf.Ticker("SPY")
print("Elapsed time for Ticker")
count_time(timer)

#timer = time.time()
#info = stock.info
#print(info)
# This took roughly 210 seconds

timer = time.time()
data = stock.history()
print(data)
count_time(timer)
# This took roughly 40 seconds

timer = time.time()
data = stock.history(period="1d", interval="5m", prepost=True)
print(data)
count_time(timer)


timer = time.time()
jsondata = data.to_json()
print(jsondata)
count_time(timer)


