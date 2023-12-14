#!/usr/bin/python3
from flask import Blueprint, render_template, request
from models.recipe import Recipe

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    """handles the about route"""
    return render_template("home_page.html")


@main.route("/recipes")
def recipes():
    """handles the home route"""
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).all()
    return render_template("recipes.html", posts=recipes)


@main.route("/search")
def search():
    """search functionality route"""
    search_term = request.args.get("search")

    recipes = Recipe.query.filter(Recipe.title.like(f"%{search_term}%")).all()
    return render_template("search_results.html", title="Search Results", recipes=recipes)
