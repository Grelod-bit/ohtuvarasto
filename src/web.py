import math
from functools import partial

from flask import Flask, redirect, render_template, request, url_for

from varasto import Varasto


def create_app():
    app = Flask(__name__)
    inventory = {}
    routes = [
        ("/", "index", _show_inventory, ["GET"]),
        ("/items", "create_item", _create_item, ["POST"]),
        (
            "/items/add",
            "add_item",
            partial(_update_item, action="add"),
            ["POST"],
        ),
        (
            "/items/remove",
            "remove_item",
            partial(_update_item, action="remove"),
            ["POST"],
        ),
    ]
    for rule, endpoint, view, methods in routes:
        app.add_url_rule(
            rule, endpoint, partial(view, inventory), methods=methods
        )

    return app


def _show_inventory(inventory, error=None, status=200):
    return (
        render_template("index.html", inventory=inventory, error=error),
        status,
    )


def _get_quantity():
    try:
        quantity = float(request.form.get("quantity", ""))
    except ValueError:
        return None

    if not math.isfinite(quantity) or quantity < 0:
        return None
    return quantity


def _create_item(inventory):
    name = request.form.get("name", "").strip()
    quantity = _get_quantity()
    if not name or quantity is None:
        return _show_inventory(
            inventory, "Enter a name and a valid non-negative quantity.", 400
        )
    if name in inventory:
        return _show_inventory(
            inventory, "An item with that name already exists.", 400
        )

    inventory[name] = Varasto(float("inf"), quantity)
    return redirect(url_for("index"))


def _update_item(inventory, action):
    name = request.form.get("name", "")
    quantity = _get_quantity()
    if name not in inventory or quantity is None:
        return _show_inventory(
            inventory,
            "Select an item and enter a valid non-negative quantity.",
            400,
        )

    if action == "add":
        inventory[name].lisaa_varastoon(quantity)
    else:
        inventory[name].ota_varastosta(quantity)
    return redirect(url_for("index"))


if __name__ == "__main__":
    create_app().run()
