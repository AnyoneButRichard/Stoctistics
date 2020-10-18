Stoctistics
===========
An application that keeps track of historical ticker and options data.

------------------------------------------------------------------------------------------------------------------------------------------
## Version History
+ **\[v0.1.0\]** Establish a connection to the database<br>
+ **\[v0.1.1\]** Scrape stock history using yfinance<br>
+ **\[v0.1.2\]** Json storage format for stocks<br>
    + **\[v0.1.2.1\]** rstocks format<br>
    + **\[v0.1.2.2\]** astocks format<br>
+ **\[v0.1.5\]** Convert dataframe into desired json format<br>
+ **\[v0.1.9\]** Upload documents into the database<br>
+ **\[v0.2.0\]** Timings have been implemented<br>
+ **\[v0.2.3\]** Modifications of rstocks format<br>
+ **\[v0.2.5\]** Automate data collection (removing to implement cron jobs)<br>
+ **\[v0.3.0\]** Multithreading<br>
+ **\[v0.3.3\]** Cron Job added<br>
+ **\[v0.4.0\]** Refactor Functional code design into OOP design<br>
+ **\[v0.4.1\]** Stocks format is now using the bucket design pattern which is optimal for time series<br>
+ **\[v0.4.2\]** Migrated to local db server<br>
+ **\[v0.4.3\]** Added visualizations/aggregations of data using MongoDBCompass<br>
+ **\[v0.4.4\]** New authorization configuration file<br>
+ **\[v0.4.5\]** Pushing json onto the documents instead of overwriting document every time<br>
+ **\[v0.4.6\]** Complete code refactor and generated new helper classes, log.py, timer.py, regex.py, and database.py<br>
+ **\[v0.4.7\]** Multithreading has been reimplemented<br>
+ **\[v0.4.8\]** Flexible Retrieval from database with queries has been implemented<br>
+ **\[v0.5.0\]** Several Options Designs implemented and testing for metrics.<br>
    + **\[v0.5.0.1\]** nest expiry | nest strike format<br>
    + **\[v0.5.0.2\]** id expiry | nest strike format<br>
    + **\[v0.5.0.3\]** nest expiry | id strike format<br>
    + **\[v0.5.0.4\]** id expiry | id strike format<br>
+ **\[v0.5.1\]** Using built-in thread-pooling for pymongo<br>
+ **\[v0.5.2\]** Cron Job implemented for options<br>
<br>

## Milestones to reach

- Generate an options document format that can maintain
- A website that can display ticker & options data with scrubbing
- A backend API that can handle requests from the website and return appropriate data from the database
- Generate a cache 

## Current Tasks

- System redesign to accomodate for long term issues
- Measuring metrics for which options format to use
- Update strikes list and expiries list once at the beginning of every day
------------------------------------------------------------------------------------------------------------------------------------------
<br>

## Timing Reports
<br>
<br>

#### Stocks: Functional v\[0.3.0\] vs Class Design v\[0.4.6\]
|                   	| 1 stock/cycle 	| S&P 500/cycle 	|
|-------------------	|:-------------:	|:-------------:	|
| Functional Design 	|  1.08 seconds 	| 64.39 seconds 	|
| Class Design      	| 0.67 seconds  	| 28.45 seconds 	|
<br>
<br>

#### Stocks: Multithreading (16 threads) \[v0.3.0\]
|                	| 1 stock / 1 day 	| 1 stock / 60 days 	|   S&P 500 / 1 day   	|   S&P 500 / 60 days   	|
|----------------	|:---------------:	|:-----------------:	|:-------------------:	|:---------------------:	|
| rstocks format 	|  1.083 seconds  	|   32.08 seconds   	| 1 minute. 5 seconds 	| 16 minutes 36 seconds 	|
| astocks format 	|  1.066 seconds  	|   33.02 seconds   	|  1 minute 4 seconds 	|  17 minutes 6 seconds 	|
<br>
<br>

#### Stocks: Improved serialization v\[0.2.3\]
|                	| 1 stock / 1 day 	| 1 stock / 60 days 	|    S&P 500 / 1 day   	|   S&P 500 / 60 days   	|
|----------------	|:---------------:	|:-----------------:	|:--------------------:	|:---------------------:	|
| rstocks format 	|  1.146 seconds  	|   6.979 seconds   	| 9 minutes 29 seconds 	| 57 minutes 48 seconds 	|
| astocks format 	|  1.101 seconds  	|   6.357 seconds   	|  9 minutes 7 seconds 	| 52 minutes 39 seconds 	|
<br>
<br>

#### Stocks: Initial v\[0.1.2\]
|                	| 1 stock / 1 day 	| 1 stock / 60 days 	|     S&P 500 / 1 day    	|   S&P 500 / 60 days   	|
|:--------------:	|:---------------:	|:-----------------:	|:----------------------:	|:---------------------:	|
| rstocks format 	|  15.07 seconds  	|   753.34 seconds  	| 124 minutes 49 seconds 	|       not tested      	|
| astocks format 	|   1.28 seconds  	|    8.32 seconds   	|  10 minutes 37 seconds 	| 68 minutes 55 seconds 	|
<br>
<br>

Note: 60 day periods cost drastically more time. This is most likely due to limitations of the cpu.<br>
Multithreading speeds up I/O requests which we can see with the S&P 500 Index. However since a large<br>
chunk of the time was due to a **cpu bound process** (serializing the 60 day period dataframe), the cpu<br>
was most likely overworked trying to serialize all 16 threads at once. A few solutions for this would<br>
be to either **reduce the number of threads** or **execute the script sequentially**.
<br>
<br>

----------------------------------------------------------------------------------------------------------------------
<br>

## Variables & Descriptions:
To help with interpreting the code a bit more as there's no clarification of variables.

<br>
<br>


------------------------------------------------------------------------------------------------------------------------------------------
<br>

## Document Formatting:
Note: *2020-04-22T13:30:00.000+00:00* is a timestamp

### stocks (bucket design) \[v0.4.1\]
*current*
```
{
    _id: "AAL - 06/19/20",
    Symbol: "AAL",
    Date: "06/19/20",
    history:
    [
        {
            Timestamp: "2020-06-19T13:30:00.000+00:00",
            High: 250.00,
            Low: 200.00,
            Open: 225.00,
            Close: 200.00,
            Dividends: 0,
            Stock Splits: 0,
            Volume: 3273991,
        },
        {
            Timestamp: "2020-06-19T13:31:00.000+00:00",
            High: 260.00,
            Low: 210.00,
            Open: 225.00,
            Close: 200.00,
            Dividends: 0,
            Stock Splits: 0,
            Volume: 3273991,
        }, ...
    ]
}
```

### rstocks \[v0.1.2\]
*dismissed*
```
{
    "_id": "2020-04-22T13:30:00.000+00:00",
    "Close": 200.00,
    "Dividends": 0,
    "High": 250.00,
    "Low": 200.00
    "Open": 225.00,
    "Stock Splits": 0,
    "Symbol": "AAL",
    "Time": "13:30:00"
    "Timestamp": "2020-04-22T13:30:00.000+00:00",
    "Volume": 3273991
}
```
<br>
<br>

### rstocks\[v0.2.3\]
*dismissed*
```
{
    "_id": "06/19/20",
    "Close": [4000, 5000, 6000, ...],
    "Date": "06/19/20",
    "Dividends": [0, 0, 0, ...],
    "High": [5000, 6000, 7000, ...],
    "Low": [4000, 5000, 6000, ...],
    "Open": [5000, 6000, 7000, ...],
    "Stock Splits": [0, 0, 0, ...],
    "Symbol": "SPY",
    "Time": ["08:00", "08:05", "08:10", ...],
    "Timestamp": ["2020-04-22T13:30:00.000+00:00", ...],
    "Volume": [161691, 96106, 59599, ...]
}
```
<br>
<br>

### astocks \[v0.1.2\]
*dismissed*
```
{
    "_id": "SPY - 06/19/20",
    "Close": [4000, 5000, 6000, ...],
    "Date": "06/19/20",
    "Dividends": [0, 0, 0, ...],
    "High": [5000, 6000, 7000, ...],
    "Low": [4000, 5000, 6000, ...],
    "Open": [5000, 6000, 7000, ...],
    "Stock Splits": [0, 0, 0, ...],
    "Symbol": "SPY",
    "Time": ["08:00", "08:05", "08:10", ...],
    "Timestamp": ["2020-04-22T13:30:00.000+00:00", ...],
    "Volume": [161691, 96106, 59599, ...]
}
```
