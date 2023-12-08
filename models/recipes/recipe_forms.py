#!/usr/bin/python3
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired


class NewRecipe(FlaskForm):
    """A new recipe class/form"""
    title =  StringField(
        "Recipe Name",
        validators=[DataRequired()],
    )

    picture = FileField(
        "Upload Food Pic",
        validators=[
            FileAllowed([
                "jpg",
                "jpeg",
                "png",
            ])
        ]
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
