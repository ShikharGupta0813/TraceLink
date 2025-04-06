from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# SQLite DB URI
app.config['SECRET_KEY'] = "yufg567675678v"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from hack import routes