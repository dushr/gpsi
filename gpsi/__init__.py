from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='postgres://localhost/gpsi'
))

db = SQLAlchemy(app)
