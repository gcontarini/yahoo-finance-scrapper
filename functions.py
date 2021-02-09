from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
from selenium import webdriver
from time import sleep

def balance(ticker, wd_path):
    '''
    Uses selenium webdriver to open the Yahoo Finance
    balance sheet page and expand all possibles rows. 
    Then, download the newest information available.
      
    Args:
    -------
        ticker (str): must use the same ticker as Yahoo Finance
        wd_path (str): absolute path to webdriver executable
        
    Returns:
    -------
        pd.DataFrame: Balance sheets data
    '''
    
    # Web page
    url = 'https://finance.yahoo.com/quote/{}/balance-sheet?p={}'.format(ticker, ticker)
    
    # Open webdriver
    browser = webdriver.Chrome(executable_path=wd_path)
    
    # Open page
    browser.get(url)
    sleep(2)
    
    # Expand all possible rows
    cols = []
    # Try clicking in everything possible 5 times
    for i in range(5):
        rows = browser.find_elements_by_css_selector('div[data-test="fin-row"]')
    
        for r in rows:
            col_name = r.find_element_by_css_selector('span')
            
            # Dont click the same col twice
            if col_name.text not in cols:
                cols.append(col_name.text)    
            
                # Cant click, not a problem just keep clicking
                try:
                    press = r.find_element_by_css_selector('svg')
                    press.click()
                    # print('CLICKED ON: ' + col_name.text)
                    sleep(1)
                    
                except:
                    # print('NOT CLICKED IN: ' + col_name.text)
                    pass
    
    # Now we finally take the data we want
    raw_dict = {}              
    rows = browser.find_elements_by_css_selector('div[data-test="fin-row"]')
    
    for r in rows:
        # Take the data
        info = r.find_element_by_css_selector('div[data-test="fin-col"] > span')
        # Column name
        col_name = r.find_element_by_css_selector('div[title] > span')
        
        raw_dict[col_name.text] = [info.text]
    
    # Close webdrive
    browser.quit()
    
    # Convert to dict to df and values to numbers
    bs = pd.DataFrame.from_dict(raw_dict)
    bs = bs.replace(',', '', regex=True)
    bs = bs.astype('double')
    # All values are in thousand
    bs = bs * 1000
    
    return bs

def balance_allyears(ticker, wd_path):
    '''
    Uses selenium webdriver to open the Yahoo Finance
    balance sheet page and expand all possibles rows. 
    Then, download fundamental information for all years 
    available.
      
    Args:
    -------
        ticker (str): must use the same ticker as yahoo finance
        wd_path (str): absolute path to webdriver executable
        
    Returns:
    -------
        pd.DataFrame: Balance sheets data (each row is a year)
    '''
    
    # Web page
    url = 'https://finance.yahoo.com/quote/{}/balance-sheet?p={}'.format(ticker, ticker)
    
    # Open webdriver
    browser = webdriver.Chrome(executable_path=wd_path)
    
    # Open page
    browser.get(url)
    sleep(2)
    
    
    # Expand all possible rows
    cols = []
    # Try clicking in everything possible 5 times
    for i in range(5):
        rows = browser.find_elements_by_css_selector('div[data-test="fin-row"]')
    
        for r in rows:
            col_name = r.find_element_by_css_selector('span')
            
            # Dont click the same col twice
            if col_name.text not in cols:
                cols.append(col_name.text)    
                
                # Cant click, not a problem just keep clicking
                try:
                    press = r.find_element_by_css_selector('svg')
                    press.click()
                    # print('CLICKED ON: ' + col_name.text)
                    sleep(1)
                    
                except:
                    # print('NOT CLICKED IN: ' + col_name.text)
                    pass
    
    # Now we finally take the data we want
    raw_dict = {}              
    rows = browser.find_elements_by_css_selector('div[data-test="fin-row"]')
    
    for r in rows:
        # Take the data
        info = r.find_elements_by_css_selector('div[data-test="fin-col"]')
        # Column name
        col_name = r.find_element_by_css_selector('div[title] > span')
        
        info_l = []
        
        for inf in info[:4]:
            info_l.append(inf.text)
        
        raw_dict[col_name.text] = info_l
    
    # Close webdrive
    browser.quit()
    
    # Convert to dict to df and values to numbers
    bs = pd.DataFrame.from_dict(raw_dict)
    bs = bs.replace(',', '', regex=True)
    bs = bs.replace('^-$', np.nan, regex=True)
    bs = bs.astype('double')
    # All values are in thousand
    bs = bs * 1000
    
    return bs

def financials(ticker):
    '''
    Opens financials page from Yahoo Finance and download
    the newest available data.
    
    Args:
    ------
        ticker (str): must use the same ticker as Yahoo Finance
        
    Returns:
    ------
        pd.DataFrame: Financials page data
    '''

    # Web page - Financial page
    url = 'https://finance.yahoo.com/quote/{}/financials?p={}'.format(ticker, ticker)
    
    # Make the request for html page
    page = requests.get(url)
    page_content = page.content
    # Open it as a BeatifulSoup object
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Now the black magic starts
    table = soup.find_all('div', attrs={'class': 'D(tbrg)'})
    
    rows = table[0].find_all('div', attrs={'data-test': 'fin-row'})
    
    data_dict = {}
    for row in rows:
        inside_row = row.find_all('span')
        col = inside_row[0].get_text()
        data_dict[col] = [inside_row[1].get_text()]
    
    # Convert to dict to df and values to numbers
    fp = pd.DataFrame.from_dict(data_dict)
    fp = fp.replace(',', '', regex=True)
    fp = fp.astype('double')
    # All values are in thousand
    fp = fp * 1000
    
    return fp

def financials_allyears(ticker):
    '''
    Opens financials page from Yahoo Finance and download
    all available data.
    
    Args:
    ------
        ticker (str): must use the same ticker as yahoo finance
        
    Returns:
    ------
        pd.DataFrame: Financials page data (each row is a year)
    '''

    # Web page - Financial page
    url = 'https://finance.yahoo.com/quote/{}/financials?p={}'.format(ticker, ticker)
    
    # Make the request for html page
    page = requests.get(url)
    page_content = page.content
    # Open it as a BeatifulSoup object
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Now the black magic starts
    table = soup.find_all('div', attrs={'class': 'D(tbrg)'})
    
    rows = table[0].find_all('div', attrs={'data-test': 'fin-row'})
    
    data_dict = {}
    for row in rows:
        # Select data
        inside_row = row.select('div[data-test="fin-col"]')
        # Select column name
        col = row.select('div[title] > span')[0].get_text()
        
        info = []
        # Takes all data until the third element
        # After that the data is redundant
        for inf in inside_row[:4]:
            info.append(inf.get_text())
        
        # Dict to hold all data
        data_dict[col] = info
    
    # Convert to dict to df and values to numbers
    fp = pd.DataFrame.from_dict(data_dict)
    fp = fp.replace(',', '', regex=True)
    fp = fp.replace('^-$', np.nan, regex=True)
    fp = fp.astype('double')
    # All values are in thousand
    fp = fp * 1000
    
    return fp

def cashflow(ticker):
    '''
    Opens cash flow page from Yahoo Finance and takes
    the newest available data.
    
    Args:
    ------
        ticker (str): must use the same ticker as Yahoo Finance
        
    Returns:
    ------
        pd.DataFrame: Cashflow page data
    '''
    
    # Web page - Cash flow page
    url = 'https://finance.yahoo.com/quote/{}/cash-flow?p={}'.format(ticker, ticker)
    
    # Make the request for html page
    page = requests.get(url)
    page_content = page.content
    # Open it as a BeatifulSoup object
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Again, same witchcraft
    table = soup.find_all('div', attrs={'class': 'D(tbrg)'})
    
    rows = table[0].find_all('div', attrs={'data-test': 'fin-row'})
    
    data_dict = {}
    for row in rows:
        inside_row = row.find_all('span')
        col = inside_row[0].get_text()
        data_dict[col] = [inside_row[1].get_text()]
    
    # Convert to dict to df and values to numbers
    cf = pd.DataFrame.from_dict(data_dict)
    cf = cf.replace(',', '', regex=True)
    cf = cf.astype('double')
    # All values are in thousand
    cf = cf * 1000
    
    return cf

def cashflow_allyears(ticker):
    '''
    Opens cash flow page from Yahoo Finance and download
    all available data.
    
    Args:
    ------
        ticker (str): must use the same ticker as yahoo finance
        
    Returns:
    ------
        pd.DataFrame: Cashflow page data (each row is a year)
    '''

    # Web page - Cash flow page
    url = 'https://finance.yahoo.com/quote/{}/cash-flow?p={}'.format(ticker, ticker)
    
    # Make the request for html page
    page = requests.get(url)
    page_content = page.content
    # Open it as a BeatifulSoup object
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Again, same witchcraft
    table = soup.find_all('div', attrs={'class': 'D(tbrg)'})
    
    rows = table[0].find_all('div', attrs={'data-test': 'fin-row'})
    
    data_dict = {}
    for row in rows:
        # Select data
        inside_row = row.select('div[data-test="fin-col"]')
        # Select column name
        col = row.select('div[title] > span')[0].get_text()
        
        info = []
        # Takes all data until the third element
        # After that the data is redundant
        for inf in inside_row[:4]:
            info.append(inf.get_text())
        
        # Dict to hold all data
        data_dict[col] = info
    
    # Convert to dict to df and values to numbers
    cf = pd.DataFrame.from_dict(data_dict)
    cf = cf.replace(',', '', regex=True)
    cf = cf.replace('^-$', np.nan, regex=True)
    cf = cf.astype('double')
    # All values are in thousand
    cf = cf * 1000
    
    return cf

def keystats(ticker):
    '''
    Opens key statistics from Yahoo Finance and takes
    the newest available data.
    
    Args:
    ------
        ticker (str): must use the same ticker as yahoo finance
        
    Returns:
    ------
        pd.DataFrame: Key statistics page data
    '''
    
    # Web page - Key statistics
    url = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(ticker, ticker)
    # Make the request for html page
    page = requests.get(url)
    page_content = page.content
    # Open it as a BeatifulSoup object
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # It starts with a similar code from before
    table = soup.find_all('table')
    
    rows = table[0].find_all('tr')
    
    raw_data = {}
    for r in rows:
        i = r.find_all('td')
        if i:
            raw_data[i[0].get_text()] = [i[1].get_text()]
            
    # It has 2 more bottom tables with different formatation
    bottom_table = soup.select('section[data-test] > div[class] > div[class]')

    for t in bottom_table[1:]:    
        rows = t.select('table[class] > tbody > tr[class]')
        
        for r in rows:
            info = r.select('td[class]')
            raw_data[info[0].get_text().strip()] = [info[1].get_text()]
                
    # Convert to dict to df and values to numbers
    ks = pd.DataFrame.from_dict(raw_data)
    
    # Clean df
    ks = ks.replace('T', 'e+18', regex=True)
    ks = ks.replace('B', 'e+12', regex=True)
    ks = ks.replace('M', 'e+06', regex=True)
    ks = ks.replace('k', 'e+03', regex=True)
    ks = ks.replace('%', 'e-2', regex=True)
    ks = ks.replace('N/A', np.nan, regex=True)
    
    # Select not numerical columns
    notnum = ['Fiscal Year Ends', 'Most Recent Quarter (mrq)']
    for col in ks.columns:
        if 'Date' in col or 'Split' in col:
            notnum.append(col)
    date_columns = ks[notnum]
    
    # Remove not numerical cols
    ks = ks.drop(columns=notnum)
    
    # Transform numerical cols
    ks = ks.replace(',', '', regex=True)
    ks = ks.astype('double')
    
    # Join df
    ks = pd.concat([date_columns, ks], axis=1)
    
    return ks

def download_newest(ticker_list, wd_path, save_csv=False):
    '''
    Uses the functions above to download all newest 
    available data on a given stock list. Can save data
    as csv or return it as a dataframe 
    
    Args:
    ------
        ticker (str): must use the same ticker as Yahoo Finance
        wd_path (str): absolute path to webdriver executable
    
    Returns:
    ------
        pd.DataFrame: With all available data on stock
    '''

    # Dict to store data
    all_data = {}

    # Start process
    for ticker in ticker_list:
        print('#######', ticker, '#######')
        
        bs = balance(ticker, wd_path)
        sleep(1)
        fp = financials(ticker)
        sleep(1)
        cf = cashflow(ticker)
        sleep(1)
        ks = keystats(ticker)
        
        # Concat data
        data = pd.concat([bs, fp, cf, ks], axis=1)
        data.index = [ticker]

        # Append to dict of dfs
        all_data[ticker] = data
    
        # Wait
        sleep(1)

    # Join all stocks on same df
    concat = []
    for ticker in ticker_list:
        # Drop duplicate columns
        all_data[ticker] = all_data[ticker].loc[:, ~all_data[ticker].columns.duplicated()]
        concat.append(all_data[ticker])
    
    final_df = pd.concat(concat, axis=0, join='outer')

    # Save data as csv
    # Each stock is a row
    if save_csv:
        final_df.to_csv('yf_fundamental_data.csv')

    return final_df