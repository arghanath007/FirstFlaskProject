from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///market.db'
app.config['SECRET_KEY']='0e4c7ff554460dfc9e4e0a20a3b2ef'
app.config['DEBUG']=True
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category='info'

from market import  routes