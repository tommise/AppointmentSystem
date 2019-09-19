from flask import render_template, request, redirect, url_for
  
from application import app, db
from application.auth.models import User
from application.signup.forms import SignUpForm

@app.route("/signup/", methods = ["GET", "POST"])
def signup_new():

    form = SignUpForm(request.form)
    
    if not form.validate():
        return render_template("signup/signupform.html", form = form)

    name = form.name.data
    username = form.username.data
    password = form.password.data

    t = User(name, username, password, 0)
    db.session.add(t)
    db.session.commit()

    return redirect(url_for("auth_login"))