#!/usr/bin/python3
"""
This is the entry point for the kenya dishes app
"""
from flask import Flask, render_template, url_for, flash, redirect
from forms import Register, LogIn

app = Flask(__name__)
app.config["SECRET_KEY"] = "94ea6045ce05b24cf5e05cfecdcc3913"

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

    if form.validate_on_submit():
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
    return render_template("login.html", title="Log In", form=form)


if __name__ == "__main__":
    app.run(debug=True)
