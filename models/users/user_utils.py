#!/usr/bin/python3
from flask import url_for, current_app
from flask_mail import Message
from models import mail
from PIL import Image
from secrets import token_hex
import os


def save_picture(form_picture, folder, size):
    hex = token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    pic_filename = hex + ext
    pic_path = os.path.join(current_app.root_path, f"static/images/{folder}", pic_filename)

    new_size = size
    image = Image.open(form_picture)
    image.thumbnail(new_size)

    image.save(pic_path)
    return pic_filename


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