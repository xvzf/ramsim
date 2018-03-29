from importlib import import_module
from flask import Blueprint, Flask


def create_blueprint(name: str, import_name: str):
    return Blueprint(name, import_name, static_folder="static", template_folder="templates")


def register_blueprint(app: Flask, name: str, url_prefix: str):
    blueprint = getattr(
        import_module( f"ramsim.blueprints.{name}"),
            "blueprint"
        )

    if app.config["DEBUG"] == True:
        app.logger.debug(f"[{__name__}] Registering blueprint {name} to prefix {url_prefix}")

    app.register_blueprint(blueprint, url_prefix=url_prefix)
