#!/usr/bin/python3
"""routes module"""
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from models import app, db, bcrypt, mail
from models.forms import Register, LogIn, NewRecipe, RequestPasswordReset, ResetPassword
from models.recipe import Recipe
from models.user import User

with app.app_context():
    db.create_all()


def send_password_reset_email(user):
    token = user.reset_token()
    message = Message(
        "Request for Password Reset",
        sender="noreply@example.com",
        recipients=[user.email],
    )
    message.body = f'''To reset password, follow the link below

{url_for('reset_password', token=token, _external=True)}

If you did not make this request, ignore this email.
'''
    
    mail.send(message)

@app.route("/")
@app.route("/home")
def home():
    """handles the home route"""
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).all()
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
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).filter_by(user=current_user).all()
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

    return render_template("new_recipe.html", title="New Recipe", form=form, legend="New Recipe")


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


@app.route("/recipe/<int:recipe_id>/update", methods=["GET", "POST"])
@login_required
def update_recipe(recipe_id):
    """route to update a single recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user != current_user:
        abort(403)

    form = NewRecipe()

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data + request.form.getlist('ingredients[]')
        recipe.instructions = form.instructions.data + request.form.getlist('instructions[]')
        db.session.commit()

        flash(
            "Recipe updated successfully",
            "success"
        )
        return redirect(url_for("recipe", recipe_id=recipe.id))
    elif request.method == "GET":
        form.title.data = recipe.title

        while len(form.ingredients.entries) < len(recipe.ingredients):
            form.ingredients.append_entry()

        for i, ingredient in enumerate(recipe.ingredients):
            form.ingredients.entries[i].data = ingredient

        while len(form.instructions.entries) < len(recipe.instructions):
            form.instructions.append_entry()

        for i, instruction in enumerate(recipe.instructions):
            form.instructions.entries[i].data = instruction

    return render_template("new_recipe.html", title="Update Recipe", form=form, legend="Update Recipe")


@app.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    """route to delete a single recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user != current_user:
        abort(403)

    db.session.delete(recipe)
    db.session.commit()
    flash(
            "Recipe deleted successfully",
            "success"
        )
    return redirect(url_for("account"))


@app.route("/requestpasswordreset", methods=["GET", "POST"])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

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


@app.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    user = User.verify_token(token)
    if not user:
        flash(
            "That token is invalid or expired",
            "warning"
        )
        return redirect(url_for("request_password_reset"))

    form = ResetPassword()

    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hash_pwd
        db.session.commit()
        flash(
            "Your password has been successfully reset",
            "success"
        )
        return redirect(url_for("login"))

    return render_template("reset_password.html", title="Reset Password", form=form)