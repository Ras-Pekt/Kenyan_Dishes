#!/usr/bin/python3
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from models import db
from models.recipes.recipe_forms import NewRecipe
from models.recipe import Recipe

recipes = Blueprint("recipes", __name__)

@recipes.route("/recipe/new", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))

    return render_template("new_recipe.html", title="New Recipe", form=form, legend="New Recipe")


@recipes.route("/recipe/<string:recipe_id>")
def recipe(recipe_id):
    """route to return a single recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe.html", title=recipe.title, recipe=recipe)


@recipes.route("/recipe/<string:recipe_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("recipes.recipe", recipe_id=recipe.id))
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


@recipes.route("/recipe/<string:recipe_id>/delete", methods=["POST"])
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
    return redirect(url_for("users.account"))
