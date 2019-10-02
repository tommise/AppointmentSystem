from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, validators

class ServiceForm(FlaskForm):
    service = StringField("Service: ", [validators.Length(min = 5, max=100,
        message="Service field error: Please enter a service with minimum 5 characters ")])   

    price = IntegerField('Price: ', [validators.NumberRange(min=1, max=1000,
        message="Price field error: Please enter a price between 1 and 1000")])    

    class Meta:
        csrf = False

class ReserveServiceForm(FlaskForm):
    services = SelectField([validators.DataRequired()], coerce=int)

    class Meta:
        csrf = False