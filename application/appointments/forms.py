from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime

class AppointmentForm(FlaskForm):
    name = DateTimeLocalField('Time: ', default=datetime.today, format='%Y-%m-%dT%H:%M')
    class Meta:
        csrf = False

class UpdateAppointmentForm(FlaskForm):
    start_time = DateTimeLocalField('Time: ',default=datetime.today, format='%Y-%m-%dT%H:%M')
    reserved = BooleanField('Reserved: ')
    employee_id = IntegerField('Employee id: ', [validators.NumberRange(min=1, max=10, message='Enter a number minimum of 1')])

    class Meta:
        csrf = False