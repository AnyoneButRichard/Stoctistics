import scrape
import data
import time
import yfinance as yf

while(True):
    try:
        dbname = input("Enter a dbname (astocks or rstocks): ")
        tickname = input("Enter a stock ticker symbol: ")

        if(dbname != "rstocks" and dbname != "astocks"):
            raise ValueError("This is not an appropriate database")
        break
    except ValueError:
        print("Try again")

cluster = cluster_connect()                   # connect to cluster
db = cluster[dbname]                          # choose database by name
ticker = yf.Ticker(tickname)

start = time.time()

if(dbname == "rstocks"):
    collection = db[tickname]         
    add_data_rstocks(collection = collection, ticker = ticker)

elif(dbname == "astocks"):
    collection = db["stocks"]
    add_data_astocks(collection = collection, ticker = ticker)

end = time.time()
print("Transfering the data from", dbname, "took" , round(end - start, 3), "seconds")

start = time.time()

