from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from werkzeug import Response

from app.extensions import database

from .forms import AddUser
from .models import User

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"])
def all_users() -> str:
    """
    List all Users
    """
    users_lists = User.query.all()
    return render_template("users/users_lists.html", users=users_lists, title="Users")


@users.route("/<int:user_id>", methods=["GET", "POST"])
def view_user(user_id: int) -> str:
    """
    A route that allows claims officer fillout a form for a particular user
    """
    user_data = User.query.get(user_id)
    if not user_data:
        abort(404)

    return render_template("users/user_data.html", user_data=user_data)


@users.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id: int) -> Response | str:
    """
    A route for editing a user record
    """
    user_data = User.query.get(user_id)
    if not user_data:
        abort(404)

    form = AddUser()

    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(user_data)

            database.session.commit()

            flash("User updated successfully.", "success")
            return redirect(url_for("users.edit_user", user_id=user_data.id))

    return render_template("users/edit_user.html", user_data=user_data, form=form)


@users.route("/add", methods=["GET", "POST"])
def add_user() -> Response | str:
    """
    A route for adding users

    """
    form = AddUser()
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)

            database.session.add(new_user)
            database.session.commit()

            flash("User created successfully.", "success")
            return redirect(url_for("users.all_users"))

        flash("You entered and invalid form data", "danger")
        return render_template("users/create_user.html", form=form)

    return render_template("users/create_user.html", form=form)


@users.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id: int) -> Response:
    """
    A route for deleting a user
    """
    user_data = User.query.get(user_id)
    if not user_data:
        abort(404)

    database.session.delete(user_data)
    database.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("users.all_users"))
