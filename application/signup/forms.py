from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
  
class SignUpForm(FlaskForm):
    name = StringField("Name", [validators.Length(min = 2, max = 20)])
    username = StringField("Username", [validators.Length(min = 2, max = 20)])
    password = PasswordField("Password", [validators.Length(min = 2, max = 20)])
  
    class Meta:
        csrf = False