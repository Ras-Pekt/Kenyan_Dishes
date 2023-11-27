#!/usr/bin/python3
"""initialises the app"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = "94ea6045ce05b24cf5e05cfecdcc3913"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kenyan_dishes.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from models import routes
