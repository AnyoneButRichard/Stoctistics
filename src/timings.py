from scrape import *
from data import *
import time
import pandas as pd
import yfinance as yf

def generate_timings(timedata):

symbol = "UAL"
ticker = yf.Ticker(symbol)

dbnamea = "astocks"
dbnamer = "rstocks"

timinga = {"name":"astocks"}
timingr = {"name":"rstocks"}

cluster = connect()
dba = cluster[dbnamea] 
dbr = cluster[dbnamer]

collectiona = dba["collection"] 
collectionr = dbr[symbol]         

start = time.time()
df = ticker.history(period = "1d", interval = "5m")

# Individual actions
# ==================================

# Find an entry

# astock
start = time.time()
date = timestamp.strftime("%m/%d/%y")
when = timestamp.strftime("%H:%M:%S")
entry = ticker.info.symbol + " - " + date
json_day = collectiona.find_one({"_id": entry})

try: 
    found_index = json_day["Time"].index(when)
except ValueError:
    print("Not existing")

end = time.time()
timinga["find_one"] = round(end - start, 4)

# rstock
start = time.time()
timestamp = df.index[0]
collectionr.find_one({"_id":timestamp})
end = time.time()
timingr["find_one"] = round(end - start, 4)


# Aggregate actions
# ==================================

# First time adding a stock to a collection (find + insertion)

# astock
start = time.time()
add_data_astocks(collectiona, df)
end = time.time()
timinga["add_data (first)"] = round(end - start, 4)

# rstock
start = time.time()
add_data_rstocks(collectionr, df)
end = time.time()
timingr["add_data (first)"] = round(end - start, 4)

# Second time adding a stock to a collection (find)

# astock
start = time.time()
add_data_astocks(collectiona, df)
end = time.time()
timinga["add_data (second)"] = round(end - start, 4)

# rstock
start = time.time()
add_data_rstocks(collectionr, df)
end = time.time()
timingr["add_data (second)"] = round(end - start, 4)



