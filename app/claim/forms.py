from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    RadioField,
    StringField,
    TextAreaField,
    validators,
)
from wtforms.fields.choices import SelectField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList

HMO_CHOICES = [
    ("", "Select HMO"),
    ("HMO1", "HMO1"),
    ("HMO2", "HMO2"),
    ("HMO3", "HMO3"),
    ("HMO4", "HMO4"),
]
SERVICE_TYPE_CHOICES = [
    "Hematology",
    "Microbiology",
    "Chemical Pathology",
    "Histopathology",
    "Immunology",
]


class ServiceForm(FlaskForm):  # type: ignore[misc]
    service_date = DateField(format="%Y-%m-%d", validators=[validators.DataRequired()])
    service_name = StringField(
        validators=[validators.DataRequired(), validators.Length(max=100)]
    )
    service_type = RadioField(
        validators=[validators.DataRequired()], choices=SERVICE_TYPE_CHOICES
    )
    provider_name = StringField(
        validators=[validators.DataRequired(), validators.Length(max=100)]
    )
    source = StringField(
        validators=[validators.DataRequired(), validators.Length(max=100)]
    )
    cost_of_service = IntegerField(
        validators=[validators.NumberRange(min=0), validators.DataRequired()]
    )


class AddClaim(FlaskForm):  # type: ignore[misc]
    user_id = SelectField(
        "User",
        validators=[validators.DataRequired()],
    )
    diagnosis = TextAreaField(
        validators=[validators.DataRequired(), validators.Length(min=1)]
    )
    hmo = SelectField(
        validators=[validators.DataRequired(), validators.Length(max=4)],
        choices=HMO_CHOICES,
    )
    age = IntegerField(
        validators=[validators.NumberRange(min=0, max=150), validators.DataRequired()]
    )
    gender = RadioField(choices=["male", "female"], validate_choice=False)
    service_charge = IntegerField(
        validators=[validators.NumberRange(min=0), validators.DataRequired()]
    )
    total_cost = IntegerField(
        validators=[validators.NumberRange(min=0), validators.DataRequired()]
    )
    final_cost = IntegerField(
        validators=[validators.NumberRange(min=0), validators.DataRequired()]
    )
    services = FieldList(
        FormField(ServiceForm),
        validators=[validators.DataRequired()],
        min_entries=1,
    )
