from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
  
from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, SignUpForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html", form = form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()

    if not user:
        return render_template("auth/loginform.html", form = form, error = "No such username or password")

    login_user(user)
    return redirect(url_for("index")) 

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 

@app.route("/auth/signup", methods = ["GET", "POST"])
def signup_new():

    if request.method == "GET":
        return render_template("auth/signupform.html", form = SignUpForm())

    form = SignUpForm(request.form)
    
    if not form.validate():
        return render_template("auth/signupform.html", form = form)

    user_exists = User.query.filter_by(username = form.username.data).first()

    if user_exists:
        form.username.errors.append("This username is already in use. Please choose another username.")
        return render_template("auth/signupform.html", form = form)

    name = form.name.data
    username = form.username.data
    password = form.password.data

    new_user = User(name, username, password, 0)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth_login"))