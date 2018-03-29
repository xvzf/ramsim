import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .util.framework.blueprint import register_blueprint
from .util.config.routing import register_initial_redirect

db = SQLAlchemy()

def get_blueprints():
    blueprints = [
        ("core", "/core")
    ]

    for name, target in blueprints:
        yield name, target


def register_blueprints(app):
    for name, target in get_blueprints():
        register_blueprint(app, name, target)


def create_app(config_name):
    """
    @DOCSTRING TODO
    """
    app = Flask(__name__)

    # Import configuration
    cfgfile = os.path.join(os.getcwd(), "config", config_name + ".py")
    app.config.from_pyfile(cfgfile)

    # Initialize DB
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Register initial redirect
    register_initial_redirect(app)

    return app
