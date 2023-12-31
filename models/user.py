#!/usr/bin/python3
"""user class/table"""
from models import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
import uuid

def generate_id():
    return str(uuid.uuid4())


@login_manager.user_loader
def load_user(user_id):
    """
    reloads the user from user id stored in session
    """
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, default=generate_id)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    prof_pic = db.Column(db.String, nullable=False, default="default.jpg")
    password = db.Column(db.String, nullable=False)
    recipies = db.relationship("Recipe", backref="user", lazy=True)

    def reset_token(self):
        ser = Serializer(current_app.config["SECRET_KEY"])
        return ser.dumps({"user_id": self.id})

    @staticmethod
    def verify_token(token):
        ser = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = ser.loads(token)["user_id"]
            return User.query.get(user_id)
        except Exception:
            return None


    def __repr__(self):
        """remove this in final"""
        return f"User({self.id}: {self.fullname}, {self.email})"