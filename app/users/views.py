from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
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
    return render_template("users/user_data.html", user_data=user_data)


@users.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id: int) -> Response | str:
    """
    A route for editing a user record
    """
    form = AddUser()

    user_data = User.query.get(user_id)

    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        salary = request.form.get("salary")
        date_of_birth = request.form.get("date_of_birth")

        dt_obj = datetime.strptime(date_of_birth, "%Y-%m-%d")

        if form.validate_on_submit():
            user_data.name = name
            user_data.gender = gender
            user_data.salary = salary
            user_data.date_of_birth = dt_obj

            database.session.commit()

            flash("User updated successfully.", "success")
            return redirect(url_for("users.edit_user", id=user_data.id))

    return render_template("users/edit_user.html", user_data=user_data, form=form)


@users.route("/add", methods=["GET", "POST"])
def add_user() -> Response | str:
    """
    A route for adding users

    """
    form = AddUser()

    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        salary = request.form.get("salary")
        date_of_birth = request.form.get("date_of_birth")

        dt_obj = datetime.strptime(date_of_birth, "%Y-%m-%d")

        if form.validate_on_submit():
            new_user = User(
                name=name, gender=gender, salary=salary, date_of_birth=dt_obj
            )
            database.session.add(new_user)
            database.session.commit()

            flash("User created successfully.", "success")
            return redirect(url_for("users.all_users"))

        flash("You entered and invalid form data", "danger")
        return render_template("users/create_user.html", form=form)
    else:

        return render_template("users/create_user.html", form=form)


@users.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id: int) -> Response:
    """
    A route for deleting a user
    """
    user_data = User.query.get(user_id)
    database.session.delete(user_data)
    database.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("users.all_users"))
