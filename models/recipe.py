#!/usr/bin/python3
"""recipe class/table"""
from datetime import datetime
from models import db
import uuid

class Recipe(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @property
    def formatted_date(self):
        return self.date_posted.strftime("%B %d, %Y")

    def __repr__(self):
        """remove this in final"""
        return f"Recipe({self.id}: {self.title}, {self.date_posted}, {self.instructions})"