from functions import download_newest
import os

# Absolute path from work directory
path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'chromedriver'))

# Ask for user stocks input
tickers_raw = input('Tickers list separated by spaces or commas: ')

ticker_list = []
# Clean input
tickers_string = tickers_raw.replace(',', ' ')
tickers_string = tickers_string.split()
for ticker in tickers_string:
    ticker_list.append(ticker.strip())

# Download data
# And save as csv file
download_newest(ticker_list, path, True)