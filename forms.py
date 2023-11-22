#!/usr/bin/python3
"""
forms module
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Register(FlaskForm):
    """
    New member registration class/form
    """
    fullname = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=5, max=20)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


class LogIn(FlaskForm):
    """
    Existing member log in class/form
    """
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50)
        ]
    )

    remember = BooleanField("Remember Me")

    submit = SubmitField("Log In")