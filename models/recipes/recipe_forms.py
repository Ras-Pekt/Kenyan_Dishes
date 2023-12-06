#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired


class NewRecipe(FlaskForm):
    """A new recipe class/form"""
    title =  StringField(
        "Recipe Name",
        validators=[DataRequired()],
    )

    ingredients = FieldList(
        StringField(
            "Ingredient",
            validators=[DataRequired()],
        ),
        min_entries=1,
    )

    instructions = FieldList(
        StringField(
            "Instruction",
            validators=[DataRequired()],
        ),
        min_entries=1,
    )

    submit = SubmitField("Post New Recipe")
