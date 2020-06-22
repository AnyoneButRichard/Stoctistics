import json
import yfinance as yf
import time

# takes a ticker and forces its equivalent dataframe into a json object of style rstocks
def serialize_dataframe_rstocks(df, timestamp):
    i = timestamp
    json_data["_id"] = timestamp
    json_data["Symbol"] = ticker.info.symbol
    json_data["Open"] = df["Open"][i]
    json_data["Close"] = df["Close"][i]
    json_data["High"] = df["High"][i]
    json_data["Low"] = df["Low"][i]

    # This is in numpy 64int not serializable in json
    json_data["Volume"] = int(df["Volume"][i])                 
    json_data["Dividends"] = int(df["Dividends"][i]) 
    json_data["Stock Splits"] = int(df["Stock Splits"][i])
    return json_data

# takes a ticker and forces its equivalent dataframe into a json object of style astocks
def serialize_dataframe_astocks(ticker, per = "1d", inc = "5m"):

    # initializing data
    json_list = []
    json_data = {}
    json_data["_id"] = df.info.symbol + " - " + date
    json_data["Name"] = df.info.symbol
    json_data["Time"] = []
    json_data["Open"] = []
    json_data["Close"] = []
    json_data["High"] = []
    json_data["Low"] = []
    json_data["Volume"] = []
    json_data["Dividends"] = []
    json_data["Stock Splits"] = []

    # date to use and keep track of independent json objects
    date = df[0].strftime("%m/%d/%y")

    for i in df.index:

        # constantly check the date
        timestamp = i
        newdate = timestamp.strftime("%m/%d/%y")

        # new date = new object (stock name does not change)
        if(newdate != date):
            json_list.append(json_data)
            date = newdate
            json_data["_id"] = df.info.symbol + " - " + date
            json_data["Time"].clear()
            json_data["Open"].clear()
            json_data["Close"].clear()
            json_data["High"].clear()
            json_data["Low"].clear()
            json_data["Volume"].clear()
            json_data["Dividends"].clear()
            json_data["Stock Splits"].clear()

        # add information to the object
        json_data["Time"].append(timestamp.strftime("%H:%M:%S")
        json_data["Open"].append(df["Open"][i])
        json_data["Close"].append(df["Close"][i])
        json_data["High"].append(df["High"][i])
        json_data["Low"].append(df["Low"][i])
        json_data["Volume"].append(int(df["Volume"][i]))
        json_data["Dividends"].append(int(df["Dividends"][i]))
        json_data["Stock Splits"].append(int(df["Stock Splits"][i]))

    json_list.append(json_data)

    # return a list of day objects by the stock
    return json_list
