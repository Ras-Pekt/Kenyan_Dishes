#!/usr/bin/python3
from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(403)
def forbidden(error):
    return render_template("errors/forbidden.html", title="Access Denied!"), 403


@errors.app_errorhandler(404)
def not_found(error):
    return render_template("errors/not_found.html", title="Lost in the Sauce!"), 404


@errors.app_errorhandler(500)
def server_error(error):
    return render_template("errors/server_error.html", title="Server on the FRITZ!"), 500
