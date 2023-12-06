#!/usr/bin/python3
"""initialises the app"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from models.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config=Config):
    """creates an instance of the app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from models.users.user_routes import users
    from models.recipes.recipe_routes import recipes
    from models.main.routes import main
    from models.errors.error_handler import errors

    app.register_blueprint(users)
    app.register_blueprint(recipes)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
