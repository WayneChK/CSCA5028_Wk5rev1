from StockEvaluator.AppServer import App
from StockEvaluator.SQLdb import sqlite_db

# Define a function to create the app
def create_app():
    with App.app.app_context():
        sqlite_db.db.create_all()
    return App.app

# The following line is required by Gunicorn
app = create_app()

# if __name__ == "__main__":
#     with App.app.app_context():
#         sqlite_db.db.create_all()

#     from gunicorn.app.wsgiapp import WSGIApplication

#     def app(environ, start_response):
#         return App.app(environ, start_response)

#     # Use the Gunicorn application function
#     WSGIApplication(app).run()

#     #App.app.run()