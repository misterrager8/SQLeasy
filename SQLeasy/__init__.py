import mysql.connector
from flask import Flask

from SQLeasy import config

mysql_ = mysql.connector.connect(
    user=config.USER, password=config.PASSWORD, host=config.HOST
)
cursor_ = mysql_.cursor()

app = Flask(__name__)


def create_app(config):
    app.config.from_object(config)

    with app.app_context():
        from SQLeasy import views

        return app
