#!/usr/bin/python3
from flask import url_for
from flask_mail import Message
from models import mail


def save_picture(form_picture):
    pass


def send_password_reset_email(user):
    token = user.reset_token()
    message = Message(
        "Request for Password Reset",
        sender="noreply@example.com",
        recipients=[user.email],
    )
    message.body = f'''To reset password, follow the link below

{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request, ignore this email.
'''
    
    mail.send(message)