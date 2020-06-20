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
data = stock.history(period="2y", interval="60m")
print(data)
count_time(timer)

#timer = time.time()
#for i in data.index:
#    print(i)
#    print(data["High"][i])
#count_time(timer)


timer = time.time()
jsondata = {}
for i in data.index:
    jsondata[i] = data["Open"][i]
#print(jsondata)
count_time(timer)

#
#for key, value in jsondata.items():
#    print(key, ' : ', value)



