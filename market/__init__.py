from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '6e6cf3f875a3a73830d88caf'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key = '1094737348611-ql5ga54uf68h1bkhf6mulbhvomemsg13.apps.googleusercontent.com',
    consumer_secret = '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',
)

from market import routes