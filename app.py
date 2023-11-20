#!/usr/bin/python3
"""
This is the entry point for the kenya dishes app
"""
from flask import Flask, render_template, url_for

app = Flask(__name__)

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
        "title": "Ugali Matumbo",
        "ingredients": ["ugali", "matumbo"],
        "method": ["Make ugali", "cook matumbo", "serve while hot"],
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


if __name__ == "__main__":
    app.run(debug=True)
