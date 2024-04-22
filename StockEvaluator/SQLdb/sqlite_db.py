from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import pandas as pd

db = SQLAlchemy()

class stock_hist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=False) # by default, unique = False
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volume = db.Column(db.Integer, unique=True)  # use volume to detect duplication of records
    date = db.Column(db.Date, unique=False)

def add_data(ticker_i, df_stock):
    tstep = df_stock.shape[0]
    inserted_rows = 0

    for j in range(tstep):

        try:
            date_j = df_stock.index[j]
            open_j = df_stock.iloc[j,0]
            high_j = df_stock.iloc[j,1]
            low_j = df_stock.iloc[j,2]
            close_j = df_stock.iloc[j,3]
            vol_j = df_stock.iloc[j,4]
            ticker_j = ticker_i + "_" + str(j)
        
            entry_instance = stock_hist(ticker = ticker_j, date = date_j,
                                        open_price = open_j, high_price = high_j,
                                        low_price = low_j, close_price = close_j, volume = vol_j)
            db.session.add(entry_instance)
            db.session.commit()
            inserted_rows += 1
        
        except IntegrityError as e:
            db.session.rollback()
            print(f'Duplicated row at {inserted_rows}, now roll back')

    