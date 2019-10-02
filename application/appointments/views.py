from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.auth.models import User
from application.services.models import Service
from application.appointments.models import Appointment
from application.appointments.forms import AppointmentForm
from application.appointments.forms import UpdateAppointmentForm
from application.services.forms import ReserveServiceForm
from datetime import datetime

# Listing appointments

@app.route("/appointments/", methods=["GET"])
@login_required(role="ANY")
def appointments_index():
    return render_template("appointments/list.html", appointments = Appointment.query.all())

@app.route("/appointments/myappointments", methods=["GET"])
@login_required(role="ANY")
def my_appointments():
    return render_template("appointments/myappointments.html", user_reservations = Appointment.query.all())  

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
    t.accountappointment.append(user)  

    db.session().add(t)
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

    form1 = UpdateAppointmentForm()

    employees = User.query.filter_by(employee = True)
    employeelist = [(i.id, i.name) for i in employees]
    form1.employees.choices = employeelist

    users = User.query.filter_by(employee = False)
    userslist = [(i.id, i.name) for i in users]
    form1.users.choices = userslist

    return render_template("appointments/update.html", appointments = Appointment.query.all(), form = form1)

@app.route("/appointments/update/<appointment_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def appointments_updates(appointment_id):

    form = UpdateAppointmentForm(request.form)

    employees = User.query.filter_by(employee = True)
    employeelist = [(i.id, i.name) for i in employees]
    form.employees.choices = employeelist

    users = User.query.filter_by(employee = False)
    userslist = [(i.id, i.name) for i in users]
    form.users.choices = userslist
    
    if not form.validate():
        return render_template("appointments/update.html", appointments = Appointment.query.all(), form = form)

    t = Appointment.query.get(appointment_id)

    user_id = form.users.data
    employee_id = form.employees.data

    new_user = User.query.get(user_id)
    new_employee = User.query.get(employee_id)

    t.accountappointment.clear()
    t.accountappointment.append(new_user)
    t.accountappointment.append(new_employee)

    t.start_time = form.start_time.data
    t.reserved = form.reserved.data

    db.session().commit()
  
    return redirect(url_for("appointments_update"))

# Reserving an appointment

@app.route("/appointments/reserve/", methods=["GET"])
@login_required(role="ANY")
def appointments_reserve():

    form = ReserveServiceForm(request.form)

    services = Service.query.all()
    serviceslist = [(i.id, "".join(i.service + ', ' + str(i.price) + 'e')) for i in services]
    form.services.choices = serviceslist

    return render_template("appointments/reserve.html", appointments = Appointment.query.filter_by(reserved = False), form = form)

@app.route("/appointments/reserve/<appointment_id>/", methods=["POST"])
@login_required(role="ANY")
def appointment_set_reserved(appointment_id):

    form = ReserveServiceForm(request.form)

    services = Service.query.all()
    serviceslist = [(i.id, i.service) for i in services]
    form.services.choices = serviceslist    

    if not form.validate():
        return render_template("appointments/reserve.html", appointments = Appointment.query.filter_by(reserved = False), form = form)  

    user = User.query.get(current_user.id)

    t = Appointment.query.get(appointment_id)

    service_id = form.services.data
    new_service = Service.query.get(service_id)

    if t.reserved is True:
        t.reserved = False
    elif t.reserved is False:
        t.reserved = True
    
    t.services.append(new_service)
    t.accountappointment.append(user)        

    db.session().commit()
  
    return redirect(url_for("my_appointments"))    

# Cancelling an appointment

@app.route("/appointments/cancel/", methods=["GET"])
@login_required(role="ANY")
def appointments_cancel():

    return render_template("appointments/cancel.html", appointments = Appointment.query.all())

@app.route("/appointments/cancel/<appointment_id>/", methods=["POST"])
@login_required(role="ANY")
def appointment_set_cancel(appointment_id):

    t = Appointment.query.get(appointment_id)

    employee = t.accountappointment[0]
    
    t.reserved = False
    t.accountappointment.clear()

    t.accountappointment.append(employee)

    db.session().commit()
  
    return redirect(url_for("appointments_cancel"))

# Statistics

@app.route('/appointments/statistics/users_without_reservation/')
@login_required(role="ADMIN")
def users_without_reservation():
    return render_template("appointments/statistics.html", users_without_reservation = User.get_users_without_reservation())

@app.route('/appointments/statistics/most_popular_services/')
@login_required(role="ADMIN")
def most_popular_services():
    return render_template("appointments/statistics.html", most_popular_services = Appointment.get_most_popular_services())