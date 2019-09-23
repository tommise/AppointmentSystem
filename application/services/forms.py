from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, validators

class ServiceForm(FlaskForm):
    service = StringField("Service: ", [validators.Length(min = 5, max=100)])    
    price = IntegerField('Price: ', [validators.NumberRange(min=1, max=100000)])    

    class Meta:
        csrf = False