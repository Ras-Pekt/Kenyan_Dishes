#!/usr/bin/python3
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from models import db, bcrypt
from models.users.user_forms import Register, LogIn, RequestPasswordReset, ResetPassword
from models.recipe import Recipe
from models.user import User
from models.users.user_utils import send_password_reset_email

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    """register new user route"""
    form = Register()
    fullname = form.fullname.data
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(fullname=fullname, email=email, password=hash_pwd)
        db.session.add(new_user)
        db.session.commit()
        flash(
            f"{fullname.title()}'s account created successfully",
            "success"
        )
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    """existing user log in route"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LogIn()
    email = form.email.data
    password = form.password.data
    remember_me = form.remember.data

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, password):
            login_user(existing_user, remember=remember_me)

            next_param = request.args.get("next")
            if next_param:
                return redirect(next_param)
            else:
                return redirect(url_for("main.home"))
        else:
            flash(
                "Log In Unsuccessful. Check Email and Password",
                "danger"
            )
    return render_template("login.html", title="Log In", form=form)


@users.route("/logout")
def logout():
    """existing user log out route"""
    logout_user()
    return redirect (url_for("main.home"))


@users.route("/account")
@login_required
def account():
    """route to display the current user's account"""
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).filter_by(user=current_user).all()
    return render_template("account.html", title="Account", posts=recipes)


@users.route("/user/<string:user_id>")
def user(user_id):
    """route to return a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", title=user.fullname, user=user)


@users.route("/requestpasswordreset", methods=["GET", "POST"])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RequestPasswordReset()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash(
            f"Instructions to reset password have been sent to {user.email}",
            "info"
        )
        return redirect("login")

    return render_template("request_password_reset.html", title="Request Password Reset", form=form)


@users.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    user = User.verify_token(token)
    print(user)
    if not user:
        flash(
            "That token is invalid or has expired",
            "warning"
        )
        return redirect(url_for("users.request_password_reset"))

    form = ResetPassword()

    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hash_pwd
        db.session.commit()
        flash(
            "Your password has been successfully reset",
            "success"
        )
        return redirect(url_for("users.login"))

    return render_template("reset_password.html", title="Reset Password", form=form)