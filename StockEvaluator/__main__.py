from StockEvaluator.AppServer import App
from StockEvaluator.SQLdb import sqlite_db

if __name__ == "__main__":
    with App.app.app_context():
        sqlite_db.db.create_all()
    App.app.run()