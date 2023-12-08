#!/usr/bin/python3
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
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


class UpdateAccount(FlaskForm):
    """
    Update user details class/form
    """
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    picture = FileField(
        "Update Profile Picture",
        validators=[
            FileAllowed([
                "jpg",
                "jpeg",
                "png",
            ])
        ]
    )

    submit = SubmitField("Update")


    def validate_email(self, email):
        """
        checks if the email already exists in the database
        """
        if email.data != current_user.email:
            existing_email = User.query.filter_by(email=email.data).first()
            if existing_email:
                raise ValidationError("This email already has an account associated with it")


class RequestPasswordReset(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """
        checks if the email already exists in the database
        """
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email is None:
            raise ValidationError("This email is not associated with an account. Please register")


class ResetPassword(FlaskForm):
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

    submit = SubmitField("Reset Password")
