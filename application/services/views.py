from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.services.models import Service
from application.services.forms import ServiceForm

# Listing services

@app.route("/services/", methods=["GET"])
@login_required(role="ANY")
def services_list():
    return render_template("services/list.html", services = Service.query.all())

# Creating a new service

@app.route("/services/new/")
@login_required(role="ADMIN")
def services_form():
    return render_template("services/new.html", form = ServiceForm())  

@app.route("/services/", methods=["POST"])
@login_required(role="ADMIN")
def services_create():

    form = ServiceForm(request.form)

    if not form.validate():
        return render_template("services/new.html", form = form)

    t = Service(form.service.data, form.price.data)
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("services_list"))   

# Removing a service

@app.route("/service/remove/", methods=["GET"])
@login_required(role="ADMIN")
def services_remove():
    return render_template("services/remove.html", services = Service.query.all())

@app.route("/services/remove/<service_id>/", methods=["POST"])
@login_required(role="ADMIN")
def services_delete(service_id):

    t = Service.query.get(service_id)

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("services_remove")) 

# Updating a service   

@app.route("/services/update/", methods=["GET"])
@login_required(role="ADMIN")
def services_update():
    return render_template("services/update.html", services = Service.query.all(), form = ServiceForm())

@app.route("/services/update/<service_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def services_updates(service_id):

    form = ServiceForm(request.form) 

    if not form.validate():
        return render_template("services/update.html", form = form)

    t = Service.query.get(service_id)

    t.service = form.service.data
    t.price = form.price.data

    db.session().commit()
  
    return redirect(url_for("services_update"))    