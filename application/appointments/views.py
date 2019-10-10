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
    return render_template("appointments/list.html", appointments = Appointment.query.order_by(Appointment.start_time.asc()).all())

@app.route("/appointments/myappointments", methods=["GET"])
@login_required(role="ANY")
def my_appointments():
    return render_template("appointments/myappointments.html", user_reservations = Appointment.query.order_by(Appointment.start_time.asc()).all())

# Creating an appointment

@app.route("/appointments/new/")
@login_required(role="ADMIN")
def appointments_form():
    return render_template("appointments/new.html", form = AppointmentForm())

@app.route("/appointments/", methods=["POST"])
@login_required(role="ADMIN")
def appointments_create():

    employee = User.query.get(current_user.id)

    form = AppointmentForm(request.form)

    if not form.validate():
        return render_template("appointments/new.html", form = form) 

    currentYear = int(datetime.now().year)
    comparedYear = int(form.time.data.strftime('%Y'))

    # Checking if input year is smaller than current year or input year is more than two years ahead
    if currentYear > comparedYear or currentYear + 1 < comparedYear:
        form.time.errors.append("The time you picked is in the past or way too ahead in future, please choose another time.")
        return render_template("appointments/new.html", form = form)

    # Checking if employee has already created an appointment time at this starting time
    def appointmentIsUnique():
        appointmentTimes = Appointment.query.filter_by(start_time = form.time.data)

        for appointment in appointmentTimes:
            if appointment.accountappointment[0].id == current_user.id:
                return False

        return True 

    if not appointmentIsUnique():
        form.time.errors.append("You have already an appointment at this starting time, please choose another time.")
        return render_template("appointments/new.html", form = form)

    t = Appointment(form.time.data)
    t.accountappointment.append(employee)  

    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("appointments_index"))

# Removing an appointment

@app.route("/appointments/remove/", methods=["GET"])
@login_required(role="ADMIN")
def appointments_remove():
    return render_template("appointments/remove.html", appointments = Appointment.query.order_by(Appointment.start_time.asc()).all())

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
def appointments_updatelist():
    return render_template("appointments/update.html", appointments = Appointment.query.order_by(Appointment.start_time.asc()).all())

@app.route("/appointments/update/<appointment_id>/", methods=["POST"])
@login_required(role="ADMIN")
def appointments_update(appointment_id):
    
    t = Appointment.query.get(appointment_id)
    # Populating the form fields with current information

    form = UpdateAppointmentForm(obj=t)

    employees = User.query.filter_by(employee = True)
    currentemployee = t.accountappointment[0]
    employeelist = [(currentemployee.id, currentemployee.name)]
    for i in employees:
        if i.id != currentemployee.id:
            employeelist.append([i.id, i.name])
    form.employees.choices = employeelist

    customers = User.query.filter_by(employee = False)
    services = Service.query.all()

    # If the appointment is reserved, populate first with current customer
    if t.reserved is True:
        currentcustomer = t.accountappointment[1]
        customerlist = [(currentcustomer.id, currentcustomer.name)]

        for i in customers:
            if i.id != currentcustomer.id:
                customerlist.append([i.id, i.name])

    else:
        customerlist = [(i.id, i.name) for i in customers]

    # If there is a service connected to the appointment, populate
    if len(t.services) > 0:
        currentservice = t.services[0]        
        serviceslist = [(currentservice.id, "".join(currentservice.service + ', ' + str(currentservice.price) + 'e'))]

        for i in services:
            if i.id != currentservice.id:
                serviceslist.append([i.id, "".join(i.service + ', ' + str(i.price) + 'e')])
    else:
        serviceslist = [(i.id, "".join(i.service + ', ' + str(i.price) + 'e')) for i in services]        

    form.users.choices = customerlist
    form.services.choices = serviceslist

    return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

@app.route("/appointments/update/commit/<appointment_id>/", methods=["POST"])
@login_required(role="ADMIN")
def appointments_updates(appointment_id):
    
    t = Appointment.query.get(appointment_id)
    form = UpdateAppointmentForm(request.form)
    
    employees = User.query.filter_by(employee = True)
    employeelist = [(i.id, i.name) for i in employees]
    form.employees.choices = employeelist

    users = User.query.filter_by(employee = False)
    userslist = [(i.id, i.name) for i in users]
    form.users.choices = userslist
    
    services = Service.query.all()
    serviceslist = [(i.id, "".join(i.service + ', ' + str(i.price) + 'e')) for i in services]
    form.services.choices = serviceslist
    
    if not form.validate():
        render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    currentYear = int(datetime.now().year)
    comparedYear = int(form.start_time.data.strftime('%Y'))

    if not t.accountappointment[0].id == current_user.id:
        form.start_time.errors.append("You cannot update an appointment that you are not assigned to.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    # Checking if input year is smaller than current year or input year is more than two years ahead
    if currentYear > comparedYear or currentYear + 1 < comparedYear:
        form.start_time.errors.append("The time you picked is in the past or way too ahead in future, please choose another time.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    # Checking if chosen employee already has an appointment at this starting time (excluding the appointment that is being updated)
    def appointmentIsUnique():
        appointmentTimes = Appointment.query.filter_by(start_time = form.start_time.data)

        for appointment in appointmentTimes:
            if appointment is not t and appointment.accountappointment[0].id == form.employees.data:
                return False

        return True 

    if not appointmentIsUnique():
        form.start_time.errors.append("Chosen employee already has an appointment time at this starting time, please choose another time.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    # Updating the appointment
    user = User.query.get(form.users.data)
    employee = User.query.get(form.employees.data)
    service = Service.query.get(form.services.data)

    t.services.clear()
    t.accountappointment.clear()
    db.session().commit()

    t.start_time = form.start_time.data

    # If reserved is set to False, information about user and service are disregarded
    if form.reserved.data is False:
        t.accountappointment.append(employee)        
        t.reserved = form.reserved.data

        db.session().commit()        
        return redirect(url_for("appointments_updatelist"))
    
    t.accountappointment.append(employee)
    t.accountappointment.append(user)
    t.services.append(service)
    t.reserved = form.reserved.data

    db.session().commit()
  
    return redirect(url_for("appointments_updatelist"))

# Reserving an appointment

@app.route("/appointments/reserve/", methods=["GET"])
@login_required(role="ANY")
def appointments_reserve():

    form = ReserveServiceForm(request.form)

    services = Service.query.all()
    serviceslist = [(i.id, "".join(i.service + ', ' + str(i.price) + 'e')) for i in services]
    form.services.choices = serviceslist

    return render_template("appointments/reserve.html", 
        appointments = Appointment.query.filter_by(reserved = False).order_by(Appointment.start_time.asc()).all(), form = form)

@app.route("/appointments/reserve/<appointment_id>/", methods=["POST"])
@login_required(role="ANY")
def appointment_set_reserved(appointment_id):

    form = ReserveServiceForm(request.form)

    services = Service.query.all()
    serviceslist = [(i.id, i.service) for i in services]
    form.services.choices = serviceslist    

    if not form.validate():
        return render_template("appointments/reserve.html", 
        appointments = Appointment.query.filter_by(reserved = False).order_by(Appointment.start_time.asc()).all(), form = form) 

    t = Appointment.query.get(appointment_id)
    employee = t.accountappointment[0]
    t.accountappointment.clear()
    db.session().commit()    

    new_user = User.query.get(current_user.id)

    service_id = form.services.data
    new_service = Service.query.get(service_id)
    
    t.reserved = True
    t.services.append(new_service)
    t.accountappointment.append(employee) 
    t.accountappointment.append(new_user)        

    db.session().commit()
  
    return redirect(url_for("my_appointments"))    

# Cancelling an appointment

@app.route("/appointments/cancel/", methods=["GET"])
@login_required(role="ANY")
def appointments_cancel():

    return render_template("appointments/cancel.html", appointments = Appointment.query.order_by(Appointment.start_time.asc()).all())

@app.route("/appointments/cancel/<appointment_id>/", methods=["POST"])
@login_required(role="ANY")
def appointment_set_cancel(appointment_id):

    t = Appointment.query.get(appointment_id)

    employee = t.accountappointment[0]
    
    t.reserved = False
    t.accountappointment.clear()
    t.services.clear()
    db.session().commit()

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