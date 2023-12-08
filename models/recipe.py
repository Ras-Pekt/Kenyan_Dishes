#!/usr/bin/python3
"""recipe class/table"""
from datetime import datetime
from models import db
import uuid

def generate_id():
    return str(uuid.uuid4())

class Recipe(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_id)
    title = db.Column(db.String(100), nullable=False)
    recipe_pic = db.Column(db.String(20))
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @property
    def formatted_date(self):
        return self.date_posted.strftime("%B %d, %Y")

    def __repr__(self):
        """remove this in final"""
        return f"Recipe(ID:{self.id}\nTITLE:{self.title}\nDATE:{self.date_posted}\nINSTRUCTIONS{self.instructions}\nPIC{self.recipe_pic})"