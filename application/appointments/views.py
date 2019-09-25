from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.auth.models import User
from application.appointments.models import Appointment
from application.appointments.forms import AppointmentForm
from application.appointments.forms import UpdateAppointmentForm
from datetime import datetime

# Listing appointments

@app.route("/appointments/", methods=["GET"])
@login_required(role="ANY")
def appointments_index():
    return render_template("appointments/list.html", appointments = Appointment.query.all())

@app.route("/appointments/myappointments", methods=["GET"])
@login_required(role="ANY")
def my_appointments():
    return render_template("appointments/myappointments.html", user_reservations = Appointment.get_reservations_by_id(current_user.id))  

# Creating an appointment

@app.route("/appointments/new/")
@login_required(role="ADMIN")
def appointments_form():
    return render_template("appointments/new.html", form = AppointmentForm())

@app.route("/appointments/", methods=["POST"])
@login_required(role="ADMIN")
def appointments_create():

    user = User.query.get(current_user.id)

    form = AppointmentForm(request.form)

    if not form.validate():
        return render_template("appointments/new.html", form = form) 
       
    t = Appointment(form.name.data)
    # t.service_id = 
    db.session().add(t)

    t.accountappointment.append(user)

    db.session().commit()
  
    return redirect(url_for("appointments_index"))

# Removing an appointment

@app.route("/appointments/remove/", methods=["GET"])
@login_required(role="ADMIN")
def appointments_remove():
    return render_template("appointments/remove.html", appointments = Appointment.query.all())

@app.route("/appointments/remove/<appointment_id>/", methods=["POST"])
@login_required(role="ADMIN")
def appointments_delete(appointment_id):

    t = Appointment.query.get(appointment_id)

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("appointments_remove")) 

# Updating an appointment    

@app.route("/appointments/update/", methods=["GET"])
@login_required(role="ADMIN")
def appointments_update():
    return render_template("appointments/update.html", appointments = Appointment.query.all(), form = UpdateAppointmentForm())

@app.route("/appointments/update/<appointment_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
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

# Reserving and cancelling an appointment

@app.route("/appointments/reserve/", methods=["GET"])
@login_required(role="ANY")
def appointments_reserve():

    return render_template("appointments/reserve.html", appointments = Appointment.query.all())

@app.route("/appointments/reserve/<appointment_id>/", methods=["POST"])
@login_required(role="ANY")
def appointment_set_reserved(appointment_id):

    user = User.query.get(current_user.id)

    t = Appointment.query.get(appointment_id)

    if t.reserved is True:
        t.reserved = False
    elif t.reserved is False:
        t.reserved = True
    
    t.accountappointment.append(user)        

    db.session().commit()
  
    return redirect(url_for("my_appointments"))    

# Statistics

@app.route('/appointments/statistics/')
@login_required(role="ADMIN")
def admin_statistics():
    return render_template("appointments/statistics.html", users_without_reservation = User.get_users_without_reservation())