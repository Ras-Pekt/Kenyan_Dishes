#!/usr/bin/python3
"""
forms module
"""
from flask_wtf import FlaskForm
from models.user import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class Register(FlaskForm):
    """
    New member registration class/form
    """
    fullname = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=5, max=50)
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


    def validate_email(self, email):
        """
        checks if the email already exists in the database
        """
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("This email already has an account associated with it")


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