from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.appointments.models import Appointment
from application.appointments.forms import AppointmentForm
from application.appointments.forms import UpdateAppointmentForm
from datetime import datetime

@app.route("/appointments/", methods=["GET"])
@login_required
def appointments_index():
    return render_template("appointments/list.html", appointments = Appointment.query.all())

@app.route("/appointments/new/")
@login_required
def appointments_form():
    return render_template("appointments/new.html", form = AppointmentForm())

@app.route("/appointments/<appointment_id>/", methods=["POST"])
@login_required
def appointment_set_reserved(appointment_id):

    t = Appointment.query.get(appointment_id)

    db.session().commit()
  
    return redirect(url_for("appointments_index"))

@app.route("/appointments/", methods=["POST"])
@login_required
def appointments_create():

    form = AppointmentForm(request.form)

    if not form.validate():
        return render_template("appointments/new.html", form = form)    

    t = Appointment(form.name.data)
    t.account_id = current_user.id
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("appointments_index")) 

@app.route("/appointments/", methods=["POST"])
@login_required
def appointments_reserve():

    return render_template("appointments/reserve.html", appointments = Appointment.query.all()) 

## Removing an appointment

@app.route("/appointments/remove/", methods=["GET"])
@login_required
def appointments_remove():
    return render_template("appointments/remove.html", appointments = Appointment.query.all())

@app.route("/appointments/remove/<appointment_id>/", methods=["POST"])
@login_required
def appointments_delete(appointment_id):

    t = Appointment.query.get(appointment_id)

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("appointments_remove")) 

## Updating an appointment    

@app.route("/appointments/update/", methods=["GET"])
@login_required
def appointments_update():
    return render_template("appointments/update.html", appointments = Appointment.query.all(), form = UpdateAppointmentForm())

@app.route("/appointments/update/<appointment_id>/", methods=["GET", "POST"])
@login_required
def appointments_updates(appointment_id):

    form = UpdateAppointmentForm(request.form) 

    if not form.validate():
        return render_template("appointments/update.html", form = form)

    t = Appointment.query.get(appointment_id)

    t.start_time = form.start_time.data
    t.account_id = form.employee_id.data
    t.reserved = form.reserved.data

    db.session().commit()
  
    return redirect(url_for("appointments_update"))