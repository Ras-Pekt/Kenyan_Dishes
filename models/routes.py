#!/usr/bin/python3
"""routes module"""
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from models import app, db, bcrypt
from models.forms import Register, LogIn, NewRecipe
from models.recipe import Recipe
from models.user import User

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    """handles the home route"""
    recipes = Recipe.query.all()
    return render_template("home_page.html", posts=recipes)


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
    """route to display the current user's account"""
    recipes = Recipe.query.filter_by(user=current_user).all()
    return render_template("account.html", title="Account", posts=recipes)


@app.route("/recipe/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    """route for creating a new recipe"""
    form = NewRecipe()
    title = form.title.data
    ingredients = form.ingredients.data + request.form.getlist('ingredients[]')
    instructions = form.instructions.data + request.form.getlist('instructions[]')

    if form.validate_on_submit():
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user=current_user)
        db.session.add(new_recipe)
        db.session.commit()
        flash(
            "Your Recipe has been added successfully",
            "success"
        )
        return redirect(url_for("account"))

    return render_template("new_recipe.html", title="New Recipe", form=form)


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    """route to return a single recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe.html", title=recipe.title, recipe=recipe)


@app.route("/user/<int:user_id>")
def user(user_id):
    """route to return a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", title=user.fullname, user=user)