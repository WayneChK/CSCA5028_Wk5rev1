from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from datetime import datetime

from StockEvaluator.SQLdb import sqlite_db
from StockEvaluator.DataCollector import getdata
from StockEvaluator.DataAnalyzer.StockEval import Indicator_Plot


app = Flask(__name__)

# Create a Sqlite DB based on the environment: Testing or Production
env_var = "FLASK_ENV"

if (env_var in os.environ) and (os.environ[env_var] == 'testing'):
    cur_folder = os.getcwd()
    db_folder = os.path.join(cur_folder, "TestDB_storage")
else:
    cur_folder = os.getcwd()
    db_folder = os.path.join(cur_folder, "StockEvaluator/SQLdb/db_storage")

os.makedirs(db_folder, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{db_folder}/Stock.sqlite3'

# link the app configuration with sql db
sqlite_db.db.init_app(app)

#def Load_db(start_date, end_date):


@app.route('/')
def master():
    return render_template('indexpage.html')

@app.route('/endpoint_data', methods=['GET','POST'])
def fetch_data():
    if request.method == 'POST':
    
        front_fetch = request.json
        ticker_name = front_fetch["send_ticker"]
        #-----------------------------

        (df_stock, return_status) = getdata.LoadData(ticker_name)
        if not return_status:
            return jsonify(df_stock)
        
        # save dataframe data to sqlite db
        sqlite_db.add_data(ticker_name, df_stock)
        # the above will append to the existing table in the existing database

        stock_eval = Indicator_Plot(df_stock)
        fig_in_json = stock_eval.gen_plot()

      

        return jsonify({'plot':fig_in_json})

    else:
        
        return ("Please load the page from the home page")


