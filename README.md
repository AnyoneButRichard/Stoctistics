# Stoctistics
A small project for scraping and storing stocks data.

Version History
====================
+ Establish a connection to the database
+ Utilize yfinance to draw out stock history
+ Determine the storage format (astocks & rstocks)
+ Convert dataframe into desired json format
+ Be able to upload documents into the database
+ Timings Evaluation rstocks (720 seconds for 60 days), astocks (7 seconds for 60 days)
+ Reconfigured rstocks to minimize documents needed to upload
+ Automate data collection
+ Multithread to reduce time spent updating database

- cron job to run the programs in the background at the correct time and day
- Generate an options json document format
- Retrieve stock data from the database
- Reconversion back to a dataframe
- Scatter/Dot Graph of the stock data
- Generate a 1 month set focused json format [experimental]
- Change from overwriting document to appending to list inside document to reduce time [experimental]



Common Variables:
=================

**Database Connections**: 
cluster = (obj) database cluster
dbname = (str) database name
db = (obj) database
coll = (obj) collection


**YFinance**:
ticker = (obj) yfinance Ticker object
ticker_list = (list) yfinance Ticker objects
df = (obj) dataframe


**Formatting**:
symbol = (str) ticker name
symbol_list = (list) ticker names
doc = (dict) serialized json mongodb document
doc_list = (list) list of serialized json mongodb document


Json Format:
============
astocks - 1 document per stock per day
{
"_id": "SPY - 06/19/20,
"name": "SPY",
"price": [5000, 6000, 7000],
"time": ["8:00", "8:05", "8:10"]
}


rstocks - 1 document per timestamp 
{
    "_id": timestamp
    "name": "SPY"
    "Open": 100.00
    "High": 250.00
    ...
}



Timings
=======
astocks to database: 
nonexisting 1 stock over 60 days: ~ 8 seconds

rstocks to database:
nonexisting 1 stock over 60 days: ~ 720 seconds


Sources
=======
test.py source code & explanation 
(https://aroussi.com/post/python-yahoo-finance)


yfinance documentation 
(https://github.com/ranaroussi/yfinance)


pandas dataframe documentation
(https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.html)


pymongo guide with mongodb
(https://realpython.com/introduction-to-mongodb-and-python/)


pymongo collection operations
(https://api.mongodb.com/python/current/api/pymongo/collection.html)


