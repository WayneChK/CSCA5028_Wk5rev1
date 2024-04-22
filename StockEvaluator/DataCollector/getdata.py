import requests
import pandas as pd
from datetime import datetime
import os
import json

def LoadData(ticker):

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=HVAQWSZ3LHU7XOA0'
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=ACG8VVLICHJIZ6O0'
    ## this is from alphavantage.co website, needing a special apikey to get it work
    ## NOTE: this free access only allows 25 request per day. otherwise, it will return error. It tracks IP address

#===============================================
    dict_req = requests.get(url).json()
    ## retrieve stock data (daily data for this wk3 work)
#===================================================================
#=========================================================================
#   Below is for the test purpose when the 25 requests limit has been reached

    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # data_file_path = os.path.join(script_dir, 'data.json')

    # with open(data_file_path, 'r') as infile:
    #     dict_req = json.load(infile)
#====================================================================

    ## handling errors from API or ticker
    if "Error Message" in dict_req:
        return ({"error": "Check the Ticker   " + dict_req['Error Message']}, False)
    
    if not dict_req['Time Series (Daily)']:
        return ({"error":"Invalid Ticker"}, False)

    list_for_pd = []
    for (key, val) in dict_req['Time Series (Daily)'].items():  
        dateformat = "%Y-%m-%d"
        key_in_date = datetime.strptime(key, dateformat).date()
        val["datetime"] = key_in_date # add a new item into dictionary. val is a dictionary with stock prices
        list_for_pd.append(val)

    df1 = pd.DataFrame(list_for_pd)
    df1.set_index('datetime', inplace=True)
    df2 = df1.apply(pd.to_numeric)

    return (df2, True) # return pandas data frame