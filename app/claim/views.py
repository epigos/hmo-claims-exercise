import datetime as dt
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from werkzeug import Response

from app.extensions import database
from app.users.models import User

from .models import Claim, Service

claims = Blueprint("claims", __name__, url_prefix="/claims")


@claims.route("/", methods=["GET"])
def list_claims() -> str:
    """
    List all Claims
    """
    all_claims = Claim.query.all()
    return render_template("claims/claim.html", claims=all_claims, title="Claims")


@claims.route("/add", methods=["GET", "POST"])
def add_claim() -> Response | str:
    """
    A route for a claims officer to make/create a claims
    """

    if request.method == "POST":
        # Get the form field values for claims model insertion

        user = request.form.get("user")
        diagnosis = request.form.get("diagnosis")
        hmo = request.form.get("hmo")

        total_cost = request.form.get("total_cost")
        service_charge = request.form.get("service_charge")
        final_cost = request.form.get("final_cost")

        user = User.query.filter_by(name=user).first()
        new_claim = Claim(
            user_id=user.id,
            diagnosis=diagnosis,
            hmo=hmo,
            service_charge=service_charge,
            total_cost=total_cost,
            final_cost=final_cost,
        )
        database.session.add(new_claim)
        database.session.commit()

        # Get the form field values for service model insertion
        service_name = request.form.getlist("service_name")
        service_type = request.form.getlist("type")
        provider_name = request.form.getlist("provider_name")
        source = request.form.getlist("source")
        cost_of_service = request.form.getlist("cost_of_service")

        dates = request.form.getlist("service_date")

        # Formate dates
        service_date = []
        for d in dates:
            service_date.append(datetime.strptime(d, "%Y-%m-%d"))
        print("Anthony", service_date)

        # Get the above claims as foreign key for services
        claim_data = Claim.query.filter().last()

        # Loop to enter possible list of services
        for i in range(len(service_name)):
            new_service = Service(
                claim_id=claim_data.id,
                service_date=service_date[i],
                service_name=service_name[i],
                type=service_type[i],
                provider_name=provider_name[i],
                source=source[i],
                cost_of_service=cost_of_service[i],
            )
            database.session.add(new_service)
            database.session.commit()

        flash("Claim created successfully.", "success")
        return redirect(url_for("claims.claims"))
    else:
        users = User.query.with_entities(User.name).all()
        return render_template("claims/create_claim.html", all_users=users)


@claims.route("create_claim/age/", methods=["POST"])
def user_age() -> Response:
    """
    A route to get a user's birthdate
    and calculate his age
    """
    data = request.form.get("age").strip()
    user = User.query.filter_by(name=data).first()
    age = dt.date.today().year - user.date_of_birth.year
    print(age)

    return jsonify({"age": age})
