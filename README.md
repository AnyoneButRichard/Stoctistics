Stoctistics
===========
A small project started by Richard Duong and Alexi St Ana.<br>
The first step is to amass stock data and store it into a database!<br>
We haven't really decided what to do after this step.<br>

------------------------------------------------------------------------------------------------------------------------------------------
<br>

## Version History
+ **\[v0.1.0\]** Establish a connection to the datab
ase<br>
+ **\[v0.1.1\]** Scrape stock history using yfinance<br>
+ **\[v0.1.2\]** Json storage format for stocks<br>
    + **\[v0.1.23\]** rstocks format<br>
    + **\[v0.1.27\]** astocks format<br>
+ **\[v0.1.5\]** Convert dataframe into desired json format<br>
+ **\[v0.1.9\]** Upload documents into the database<br>
+ **\[v0.2.0\]** Timings have been implemented<br>
+ **\[v0.2.3\]** Modifications of rstocks format<br>
+ **\[v0.2.5\]** Automate data collection (removing to implement cron jobs)<br>
+ **\[v0.3.0\]** Multithreading<br>
<br>

## Milestones to reach
- Use a cron job to run the programs in the background at the correct time and day
- Generate an options json document format
- Retrieve stock data from the database
- Reconversion back to a dataframe
- Scatter/Dot Graph of the stock data
- (Experimental) Generate a 1 month set focused json format (increases cpu time but reduces io time)
- (Experimental) Change from overwriting document to appending to list inside document to reduce time
------------------------------------------------------------------------------------------------------------------------------------------
<br>

## Timing Reports:
We have standardized to **5 minute intervals** and **ignore premarket and aftermarket**.<br>
We also had to dismiss a few stocks from the S&P 500 Index (down to 497) to meet the requirements of Atlas:MongoDB.<br>
This will be revised back to the full 504 stocks after localizing the database.<br>

#### Initial format 6/21
|                	| 1 stock / 1 day 	| 1 stock / 60 days 	|     S&P 500 / 1 day    	|   S&P 500 / 60 days   	|
|:--------------:	|:---------------:	|:-----------------:	|:----------------------:	|:---------------------:	|
| rstocks format 	|  15.07 seconds  	|   753.34 seconds  	| 124 minutes 49 seconds 	|       not tested      	|
| astocks format 	|   1.28 seconds  	|    8.32 seconds   	|  10 minutes 37 seconds 	| 68 minutes 55 seconds 	|
<br>
<br>

#### Formatted rstocks & improved serialization
|                	| 1 stock / 1 day 	| 1 stock / 60 days 	|    S&P 500 / 1 day   	|   S&P 500 / 60 days   	|
|----------------	|:---------------:	|:-----------------:	|:--------------------:	|:---------------------:	|
| rstocks format 	|  1.146 seconds  	|   6.979 seconds   	| 9 minutes 29 seconds 	| 57 minutes 48 seconds 	|
| astocks format 	|  1.101 seconds  	|   6.357 seconds   	|  9 minutes 7 seconds 	| 52 minutes 39 seconds 	|
<br>
<br>

#### Multithreading applied (16 threads)
|                	| 1 stock / 1 day 	| 1 stock / 60 days 	|   S&P 500 / 1 day   	|   S&P 500 / 60 days   	|
|----------------	|:---------------:	|:-----------------:	|:-------------------:	|:---------------------:	|
| rstocks format 	|  1.083 seconds  	|   32.08 seconds   	| 1 minutes 5 seconds 	| 16 minutes 36 seconds 	|
| astocks format 	|  1.066 seconds  	|   33.02 seconds   	|  1 minute 4 seconds 	|  17 minutes 6 seconds 	|

Note: 60 day periods have much larger times. This is most likely due to limitations of the cpu.<br>
Multithreading speeds up I/O requests which we can see with the S&P 500 Index. However since a large<br>
chunk of the time was due to a **cpu bound process** (serializing the 60 day period dataframe), the cpu<br>
was most likely overworked trying to serialize all 16 threads at once. A few solutions for this would<br>
be to either **reduce the number of threads** or **execute the script sequentially**.

----------------------------------------------------------------------------------------------------------------------
<br>

## Variables & Descriptions:
To help with interpreting the code a bit more as there's no clarification of variables.<br>
<br>

### Database Connections 
cluster = (obj) database cluster<br>
dbname = (str) database name<br>
db = (obj) database<br>
coll = (obj) collection<br>
<br>

### YFinance
ticker = (obj) yfinance Ticker object<br>
ticker_list = (list) yfinance Ticker objects<br>
df = (obj) dataframe<br>
<br>

### Formatting
symbol = (str) ticker name<br>
symbol_list = (list) ticker names<br>
doc = (dict) serialized json mongodb document<br>
doc_list = (list) list of serialized json mongodb document<br>
<br>

### Logging
logger = (obj) an identifier logger that helps output info to a log<br>
start = (timestamp) the start time<br>
end = (timestamp) the end time<br>

------------------------------------------------------------------------------------------------------------------------------------------
<br>

## Document Formatting:
Note: *2020-04-22T13:30:00.000+00:00* is a timestamp.

### rstocks \[v0.1.2\] *dismissed*
Each collection holds all data regarding a stock<br>
Generate a document for every single 5 minute interval<br>
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

### rstocks\[v0.2.3]\] *current*
Each collection holds all data regarding a stock by day<br>
Generate a document for a day's worth of data<br>
Revision closely resembles astocks format (will be making modifications in the future to be more map-like)
\_id is the date
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

### astocks \[v0.1.2\] *current*
Each collection holds a type (historical stock data, historical options data, etc.)<br>
Generate a document for a day's worth of data<br>
List-like structure
\_id is uniquely generated by concatenating symbol with date
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
