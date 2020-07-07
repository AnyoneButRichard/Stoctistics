import yfinance as yf
import data
import scrape

dbname = input("Name of database you want to connect to: ")
cluster = data.cluster_connect()
db = cluster[dbname]
print("Prepared variables: dbname, db, ticker")
ticker = yf.Ticker("MSFT")

