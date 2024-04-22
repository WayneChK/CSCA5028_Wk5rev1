import pandas as pd
import pytest
import os


os.environ['FLASK_ENV'] = 'testing'
# set up the FLASK_ENV before importing App, as App depends on FLASK_ENV
from StockEvaluator.AppServer import App  
from StockEvaluator.SQLdb import sqlite_db

@pytest.fixture(scope = 'module')
def test_client():  
      
    
    with App.app.test_client() as client:
        yield client
   

@pytest.fixture(scope = 'module')
def test_db():
    
    with App.app.app_context():
        sqlite_db.db.create_all()
        yield sqlite_db.db
        sqlite_db.db.session.remove()

del os.environ['FLASK_ENV']
