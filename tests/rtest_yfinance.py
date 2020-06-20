import yfinance as yf
import time
import json

def count_time(time1):
    print(round(time.time() - time1, 3), "seconds")

timer = time.time()
ticker = "SPY"
stock = yf.Ticker(ticker)
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
data = stock.history(period="1mo", interval="5m")
print(data)
count_time(timer)

#timer = time.time()
#for i in data.index:
#    print(i)
#    print(data["High"][i])
#count_time(timer)


timer = time.time()
stockdate = data.index[0].strftime("%m/%d/%y")
jsondata = {}
jsondata["_id"] = ticker + " - " + stockdate
jsondata["name"] = ticker
jsondata["time"] = []
jsondata["price"] = []

for i in data.index:
    jsondata["time"].append(i.strftime("%H:%M:%S"))
    jsondata["price"].append(data["Open"][i])

print(jsondata)

#print(jsondata)
count_time(timer)

#
#for key, value in jsondata.items():
#    print(key, ' : ', value)




