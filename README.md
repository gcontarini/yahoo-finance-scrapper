# yahoo-finance-scrapper
Scripts to download fundamental data on stocks from Yahoo Finance webpage.

## Contents
In the functions file there're functions to download fundamental data from Yahoo Finance webpage. The download script is only a caller with a simple command line interface.
<br>
<br>
The functions are:
- balance: newest data on balance sheet page <br>
- balance_allyears: all available years <br>
- financials: newest data on financials page <br>
- financials_allyears: all available years <br>
- cashflow: newest data on cashflow page <br>
- cashflow_allyears: all available years <br>
- keystats: data from keystats page <br>
- download_newest: wrapper that calls functions to download only newest data on stock <br>
**Disclaimer: using the download.py to download many stocks can take while since it'll run a chrome instance for each stock.**

## Requirements
Python 3.8 <br>
BeautifulSoup4 4.9.1 <br>
Numpy 1.19.1 <br>
Pandas 1.1.0 <br>
Requests 2.24.0 <br>
Selenium 3.141.0 <br>
Google Chrome <br>
Chrome webdriver (matching your OS and chrome version) <br>

## How to use it
There're several ways to use:
- You can copy the functions script to your repository and import it.
- Use the download script.

The most important part is to download the chrome webdriver from this page: https://chromedriver.chromium.org/downloads
<br>
<br>
Unzip the driver inside your repo and name it as 'chromedriver'. It's important that the driver match your operational system and your Chrome version.
<br>
<br>
The chromedriver listed inside this repository probably will not match yours, so do your work.
<br>

## To do
- Implement option to run with firefox webdriver
- Add a docker image to run the download.py in a container