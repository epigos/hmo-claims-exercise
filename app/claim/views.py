from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from werkzeug import Response

from app.extensions import database
from app.users.models import User

from .forms import AddClaim
from .models import Claim, Service

claims = Blueprint("claims", __name__, url_prefix="/claims")


@claims.route("/", methods=["GET"])
def list_claims() -> str:
    """
    List all Claims
    """
    all_claims = Claim.query.all()
    return render_template("claims/claims.html", claims=all_claims, title="Claims")


@claims.route("/add", methods=["GET", "POST"])
def add_claim() -> Response | str:
    """
    A route for a claims officer to make/create a claims
    """
    user_choices = User.query.with_entities(User.id, User.name).all()
    user_choices = [choice.tuple() for choice in user_choices]
    user_choices.insert(0, ("", "Select user"))

    form = AddClaim()
    form.user_id.choices = user_choices

    if request.method == "POST":
        # Get the form field values for claims model insertion
        if form.validate_on_submit():
            user = User.query.get(form.data.get("user_id"))
            new_claim = Claim(
                user_id=user.id,
                diagnosis=form.data.get("diagnosis"),
                hmo=form.data.get("hmo"),
                age=form.data.get("age"),
                service_charge=form.data.get("service_charge"),
                total_cost=form.data.get("total_cost"),
                final_cost=form.data.get("final_cost"),
            )
            database.session.add(new_claim)
            database.session.commit()

            services = []
            for service_form in form.services:
                new_service = Service(
                    claim_id=new_claim.id,
                    service_date=service_form.data.get("service_date"),
                    service_name=service_form.data.get("service_name"),
                    type=service_form.data.get("service_type"),
                    provider_name=service_form.data.get("provider_name"),
                    source=service_form.data.get("source"),
                    cost_of_service=service_form.data.get("cost_of_service"),
                )
                services.append(new_service)

            database.session.add_all(services)
            database.session.commit()

            flash("Claim created successfully.", "success")
            return redirect(url_for("claims.list_claims"))

    return render_template("claims/create_claim.html", form=form)


@claims.route("/<int:claim_id>", methods=["GET"])
def view_claim(claim_id: int) -> str:
    """
    A route that allows claims officer to view claim details
    """
    claim = Claim.query.get(claim_id)
    if not claim:
        abort(404)

    return render_template("claims/claim.html", claim=claim)


@claims.route("/<int:claim_id>/delete", methods=["POST"])
def delete_claim(claim_id: int) -> Response:
    """
    A route that allows claims officer to edit claim
    """
    claim = Claim.query.get(claim_id)
    if not claim:
        abort(404)

    database.session.delete(claim)
    database.session.commit()

    flash("Claim deleted successfully.", "success")
    return redirect(url_for("claims.list_claims"))
