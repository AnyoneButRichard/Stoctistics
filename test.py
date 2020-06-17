import yfinance as yf
import time

time1 = time.time()
stock = yf.Ticker("UONEK")
time2 = time.time()
print("Elapsed time for Ticker", time2 - time1)

#stock.info
time3 = time.time()
print("Elapsed time for Info", time3 - time2)
