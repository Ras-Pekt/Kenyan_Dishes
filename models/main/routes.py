#!/usr/bin/python3
from flask import Blueprint, render_template, redirect, request
from models.recipe import Recipe

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    """handles the home route"""
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).all()
    range_len = len(recipes)
    print(range_len)
    return render_template("home_page.html", posts=recipes, len=range_len)


@main.route("/search")
def search():
    search_term = request.args.get("search")

    if search_term:
        recipes = Recipe.query.filter(Recipe.title.like(f"%{search_term}%")).all()
        return render_template("search_results.html", title="Search Results", recipes=recipes)
    return redirect("home")
