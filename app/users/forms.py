from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, RadioField, StringField, validators


class AddUser(FlaskForm):  # type: ignore[misc]
    name = StringField(
        "name",
        validators=[validators.length(min=3, max=100), validators.DataRequired()],
    )
    gender = RadioField("gender", choices=["male", "female"])
    salary = IntegerField(
        validators=[validators.NumberRange(min=0), validators.DataRequired()]
    )
    date_of_birth = DateField(format="%Y-%m-%d", validators=[validators.DataRequired()])
