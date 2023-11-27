#!/usr/bin/python3
"""routes module"""
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from models import app, db, bcrypt
from models.forms import Register, LogIn
from models.recipe import Recipe
from models.user import User

recipe_post = [
    {
        "author": "John Doe",
        "title": "Chapo Beans",
        "ingredients": ["chapo", "beans"],
        "method": ["Make chapos", "cook beans", "serve while hot"],
        "date_posted": "Nov 20, 2023",
        "date_updated": "Nov 22, 2023",
    },
    {
        "author": "Jane Doe",
        "title": "Ugali Beef",
        "ingredients": ["flour", "water", "beef", "onions", "tomatoes", "oil", "salt", "dhania"],
        "method": ["Make ugali", "cook beef", "serve while hot"],
        "date_posted": "Oct 20, 2023",
        "date_updated": "Oct 22, 2023",
    },
]

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    """handles the home route"""
    return render_template("home_page.html", posts=recipe_post)


@app.route("/about")
def about():
    """handles the about route"""
    return render_template("about_page.html", title="About")


@app.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """existing user log in route"""
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
                return redirect(url_for("home"))
        else:
            flash(
                "Log In Unsuccessful. Check Email and Password",
                "danger"
            )
    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
def logout():
    """existing user log out route"""
    logout_user()
    return redirect (url_for("home"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")