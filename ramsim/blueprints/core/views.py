from flask import render_template, url_for, redirect, request

from . import blueprint

@blueprint.route("/")
def index():
    return render_template("core/index.html")
