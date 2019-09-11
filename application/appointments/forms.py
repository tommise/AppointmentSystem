from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime

class AppointmentForm(FlaskForm):
    name = DateTimeLocalField('Time: ', default=datetime.today, format='%Y-%m-%dT%H:%M')
 
    class Meta:
        csrf = False