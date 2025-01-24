import typing

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import joinedload
from werkzeug import Response

from app.extensions import database
from app.users.models import User

from .forms import AddClaim, EditForm
from .models import Claim, Service

claims = Blueprint("claims", __name__, url_prefix="/claims")


def get_user_choices() -> list[typing.Any]:
    user_choices = User.query.with_entities(User.id, User.name).all()
    user_choices = [choice.tuple() for choice in user_choices]
    user_choices.insert(0, ("", "Select user"))
    return list(user_choices)


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
    form = AddClaim()
    form.user_id.choices = get_user_choices()

    if request.method == "POST":
        # Get the form field values for claims model insertion
        if form.validate_on_submit():
            user = User.query.get(form.user_id.data)
            new_claim = Claim(
                user_id=user.id,
                diagnosis=form.diagnosis.data,
                hmo=form.hmo.data,
                age=form.age.data,
                service_charge=form.service_charge.data,
                total_cost=form.total_cost.data,
                final_cost=form.final_cost.data,
            )
            database.session.add(new_claim)
            database.session.commit()

            services = []
            for service_form in form.services:
                new_service = Service(
                    claim_id=new_claim.id,
                    service_date=service_form.service_date.data,
                    service_name=service_form.service_name.data,
                    type=service_form.service_type.data,
                    provider_name=service_form.provider_name.data,
                    source=service_form.source.data,
                    cost_of_service=service_form.cost_of_service.data,
                )
                services.append(new_service)

            database.session.add_all(services)
            database.session.commit()

            flash("Claim created successfully.", "success")
            return redirect(url_for("claims.list_claims"))
        else:
            flash(
                "There were errors in the form. Please correct them and try again.",
                "danger",
            )

    return render_template("claims/create_claim.html", form=form)


@claims.route("/<int:claim_id>", methods=["GET"])
def view_claim(claim_id: int) -> str:
    """
    A route that allows claims officer to view claim details
    """
    claim = Claim.query.get_or_404(claim_id)

    return render_template("claims/claim.html", claim=claim)


@claims.route("/<int:claim_id>/edit", methods=["GET", "POST"])
def edit_claim(claim_id: int) -> Response | str:
    """
    A route that allows claims officer to edit claim
    """
    query_options = joinedload(Claim.services)  # type: ignore[arg-type]
    claim = Claim.query.options(query_options).get_or_404(claim_id)

    form = EditForm(obj=claim)
    form.user_id.choices = get_user_choices()

    if request.method == "POST":
        if form.validate_on_submit():
            # Update main claim fields
            claim.user_id = form.user_id.data
            claim.diagnosis = form.diagnosis.data
            claim.hmo = form.hmo.data
            claim.age = form.age.data
            claim.service_charge = form.service_charge.data
            claim.total_cost = form.total_cost.data
            claim.final_cost = form.final_cost.data
            claim.status = form.status.data
            # Clear existing services and add new ones from the form
            Service.query.filter_by(claim_id=claim.id).delete()
            # insert updated services
            updated_services = []
            for service_form in form.services.entries:
                new_service = Service(
                    claim_id=claim.id,
                    service_date=service_form.service_date.data,
                    service_name=service_form.service_name.data,
                    type=service_form.service_type.data,
                    provider_name=service_form.provider_name.data,
                    source=service_form.source.data,
                    cost_of_service=service_form.cost_of_service.data,
                )
                updated_services.append(new_service)
            # Save changes to the database
            database.session.add_all(updated_services)
            database.session.commit()
            flash("Claim updated successfully!", "success")
            return redirect(url_for("claims.view_claim", claim_id=claim_id))
        else:
            flash(
                "There were errors in the form. Please correct them and try again.",
                "danger",
            )
    else:
        form.gender.data = claim.user.gender
        form.status.data = claim.status.value
        for idx, service in enumerate(claim.services):
            form.services[idx].service_type.data = service.type
    return render_template("claims/edit_claim.html", claim=claim, form=form)


@claims.route("/<int:claim_id>/delete", methods=["POST"])
def delete_claim(claim_id: int) -> Response:
    """
    A route that allows claims officer to edit claim
    """
    claim = Claim.query.get_or_404(claim_id)

    database.session.delete(claim)
    database.session.commit()

    flash("Claim deleted successfully.", "success")
    return redirect(url_for("claims.list_claims"))
