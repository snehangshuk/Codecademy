from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# instantiate application and datbase
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# update User to inherit from UserMixin here:
class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  # add the email and password_hash attributes here:
  email = db.Column(db.String(120), unique=True, index=True)
  password_hash = db.Column(db.String(128))
  # add the joined_at attribute here
  joined_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)