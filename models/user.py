#!/usr/bin/python3
"""user class/table"""
from models import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    reloads the user from user id stored in session
    """
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recipies = db.relationship("Recipe", backref="user", lazy=True)

    def __repr__(self):
        """remove this in final"""
        return f"User({self.id}: {self.fullname}, {self.email})"