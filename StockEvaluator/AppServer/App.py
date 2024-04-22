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

print(f"App.py env var {os.environ['FLASK_ENV']}")
# link the app configuration with sql db
sqlite_db.db.init_app(app)

#def Load_db(start_date, end_date):


@app.route('/')
def master():
    return render_template('indexpage.html')

@app.route('/endpoint_data', methods=['GET','POST'])
def fetch_data():
    if request.method == 'POST':
        #------------------------------
      #  ticker_name = request.form.get(key="user_input", default="MSFT")
      #  period = request.form.get(key="time_in_days", default = 30)
      ### WE don't use the above form request this time as the front end script doesn't the entire form this time. it only sends
      ### a json string with ticker. so we do below
        front_fetch = request.json
        ticker_name = front_fetch["send_ticker"]
        #-----------------------------

        (df_stock, return_status) = getdata.LoadData(ticker_name)
        if not return_status:
            return jsonify(df_stock)
        
        # save dataframe data to sqlite db
        sqlite_db.add_data(ticker_name, df_stock)
        # the above will append to the existing table in the existing database

    #     # TEST: read the created db (select data with certain date range and load back to the endpoint)
    #     # to simplify the test, just load from database, and them convert to pandas and them save to csv. 
    #     start_date = datetime.strptime('2024-03-01', "%Y-%m-%d").date()
    #     end_date = datetime.strptime('2024-04-01', "%Y-%m-%d").date()
    #     db_model = sqlite_db.stock_hist
    #     selected_data = db_model.query.filter(db_model.date >= start_date, db_model.date <= end_date).with_entities(
    #         db_model.date, db_model.close_price
    #     )
    #     dict_list=[]
    #     for item in selected_data:
    #         dict_list.append({"date":item.date, "close_price":item.close_price})

    #     df_pick = pd.DataFrame(dict_list)
    #     df_pick.to_csv('./CSCA5028_wk5/AppServer/db_collect.csv')
    #  #   Load_db(start_date, end_date)

        stock_eval = Indicator_Plot(df_stock)
        fig_in_json = stock_eval.gen_plot()

       # return ("Data Saved and Loaded Successfully")

        return jsonify({'plot':fig_in_json})

    else:
        
        return ("Please load the page from the home page")


