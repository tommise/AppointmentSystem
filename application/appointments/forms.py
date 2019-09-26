from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime

from application.auth.models import User

class AppointmentForm(FlaskForm):
    name = DateTimeLocalField('Time: ', default=datetime.today, format='%Y-%m-%dT%H:%M')
    class Meta:
        csrf = False

class UpdateAppointmentForm(FlaskForm):
    start_time = DateTimeLocalField('Time: ',default=datetime.today, format='%Y-%m-%dT%H:%M')
    reserved = BooleanField('Reserved: ')
    employees = SelectField(coerce=int)
    users = SelectField(coerce=int)

    class Meta:
        csrf = False