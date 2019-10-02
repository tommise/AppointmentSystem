from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime

from application.auth.models import User

class AppointmentForm(FlaskForm):
    name = DateTimeLocalField("Time: ", [validators.DataRequired()], default=datetime.today, format='%Y-%m-%dT%H:%M')
    class Meta:
        csrf = False

class UpdateAppointmentForm(FlaskForm):
    start_time = DateTimeLocalField("Time: ", [validators.DataRequired()], default=datetime.today, format='%Y-%m-%dT%H:%M')
    reserved = BooleanField("Reserved: ", [validators.Optional()])
    employees = SelectField([validators.DataRequired()], coerce=int)
    users = SelectField([validators.DataRequired()], coerce=int)

    class Meta:
        csrf = False