#!/usr/bin/python3
"""initialises the app"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = "94ea6045ce05b24cf5e05cfecdcc3913"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kenyan_dishes.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
# app.config["MAIL_SERVER"] = "smtp.google.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_SERVER"] = True
# app.config["MAIL_USERNAME"] = environ.get("USER")
# app.config["MAIL_PASSWORD"] = environ.get("PASSWORD")


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True  # Use TLS for secure connection
app.config["MAIL_USE_SSL"] = False  # Do not use SSL, use TLS instead
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""

mail = Mail(app)


from models import routes
