# Stoctistics
A small project for scraping and storing stocks data.

Setup Environment Python3
==========================
1) sudo apt install python3	(python3 binary)
2) sudo apt install python3-pip		(helps install modules for python)
3) sudo apt install python3-venv (virtual environment so you can add modules without affecting global)
4) **skip** python3 -m venv python3_env (already generated virtual environment)
5) **source env/bin/activate** (enter environment)
6) **deactivate** (leave environment)

Note: be sure to run pip install only in the environment!
You'll need yfinance, pymongo, pandas, numpy, matplotlib, ...

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


**Fprmatting**:
symbol = (str) ticker name
symbol_list = (list) ticker names
document = (dict) json serialized stock dictionary
document_list = (list) list of json stock dictionaries


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


