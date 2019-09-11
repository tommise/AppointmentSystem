
from application import app, db
from flask import redirect, render_template, request, url_for
from application.appointments.models import Appointment
from application.appointments.forms import AppointmentForm
from datetime import datetime

@app.route("/appointments", methods=["GET"])
def appointments_index():
    return render_template("appointments/list.html", appointments = Appointment.query.all())

@app.route("/appointments/new/")
def appointments_form():
    return render_template("appointments/new.html", form = AppointmentForm())

@app.route("/appointments/<appointment_id>/", methods=["POST"])
def appointment_set_reserved(appointment_id):

    t = Appointment.query.get(appointment_id)

    if t.reserved is True:
        t.reserved = False
    elif t.reserved is False:
        t.reserved = True

    db.session().commit()
  
    return redirect(url_for("appointments_index"))

@app.route("/appointments/", methods=["POST"])
def appointments_create():

    form = AppointmentForm(request.form)

    t = Appointment(form.name.data)
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("appointments_index"))