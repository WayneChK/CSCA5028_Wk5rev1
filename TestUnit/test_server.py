# Unit Test for getdata.py
import pandas as pd
import requests
import unittest
from unittest.mock import patch, MagicMock
from StockEvaluator.DataCollector import getdata
# from StockEvaluator.SQLdb.sqlite_db import add_data, db
from StockEvaluator.SQLdb import sqlite_db

import datetime

class TestLoadData(unittest.TestCase):

    def setUp(self) -> None:
        self.input_dict = {'Time Series (Daily)':
                           {'2024-04-18': 
                            {'1. open': '100', '2. high': '110', '3. low': '90', '4. close': '105', '5. volume': '1000'}
                            }
                            }
        
        data_in = [[10, 20, 5, 15, 100], [11, 21, 4, 16, 120]]
        index_in = [datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1)]
        column_in = list('ohlcv')
        self.df_input = pd.DataFrame(data = data_in, index = index_in, columns = column_in)
        
    def test_fetch_data_success(self):
        with patch.object(requests, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.input_dict
            mock_get.return_value = mock_response
            df, status = getdata.LoadData('AAPL')
            self.assertTrue(status)
            self.assertEqual(df.shape[1], 5)

    def test_database_add_row(self):
        with patch.object(sqlite_db.db.session, 'add') as mock_add, \
             patch.object(sqlite_db.db.session, 'commit' ) as mock_commit :
            
            ticker_in = "AAPL"
            sqlite_db.add_data(ticker_in, self.df_input)
            # NOTE: the stock_hist class instance will be called. so must import sqlite_db to run db = SQLAlchemy().
            # or from StockEvaluator.SQLdb.sqlite_db import add_data, db. This will also work
            self.assertEqual(mock_add.call_count, 2)
            self.assertEqual(mock_commit.call_count, 2)


if __name__ == "__main__":
    unittest.main()

