from scrape import *
from data import *
import time

while(true):
    try:
        dbname = input("Enter a dbname (astocks or rstocks): ")
        ticker = input("Enter a stock ticker symbol: ")

        if(dbname != "rstocks" or dbname != "astocks"):
            raise ValueError("This is not an appropriate database")
        break
    except ValueError:
        print("Try again")


cluster = connect()             # connect to cluster
db = cluster[dbname]            # choose database by name
collection = db[ticker]         
stockdata = getHistory(ticker)

start = time.time()
if(dbname is "rstocks"):
    add_data_rstocks(collection, stockdata)
else:
    add_data_astocks(collection, stockdata)
end = time.time()
print("Using serialization:" dbname, "took" , end - start, "seconds")

