# Stoctistics
A small project for scraping and storing stocks data.

Setup Environment Python3
=======
1) sudo apt install python3	(python3 binary)
2) sudo apt install python3-pip		(helps install modules for python)
3) sudo apt install python3-venv (virtual environment so you can add modules without affecting global)
4) **skip** python3 -m venv python3_env (already generated virtual environment)
5) **source env/bin/activate** (enter environment)
6) **deactivate** (leave environment)


Setup Environment pypy3 (Not Functional! Use python3 for now)
=======
1) sudo apt-get install software-properties-common 	(adds the "add-apt-repository" command)
2) sudo apt update
3) sudo apt upgrade
4) sudo apt install pypy3
5) **skip* pypy3 -m venv pypy3_env
6) **source env/bin/activate** (enter environment)
7) **deactivate** (leave environment)


Pre-requisites for yfinance pypy3 (Not functional! Use python3 for now)
=======
- pip install cython
- pip install --upgrade setuptools
- pip install numpy
- pip install pandas


Json Format:
=======

{
"_id": "SPY - 06/19/20,
"name": "SPY",
"price": [5000, 6000, 7000],
"time": ["8:00", "8:05", "8:10"]
}



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


