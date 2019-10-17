from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.auth.models import User
from application.services.models import Service
from application.appointments.models import Appointment
from application.appointments.forms import AppointmentForm, UpdateAppointmentForm
from application.services.forms import ReserveServiceForm
from datetime import datetime

# Listing appointments

@app.route("/appointments/", methods=["GET"])
@login_required(role="ADMIN")
def appointments_index():
    return render_template("appointments/list.html", appointments = Appointment.query.order_by(Appointment.start_time.asc()).all())

@app.route("/appointments/myappointments", methods=["GET"])
@login_required(role="ANY")
def my_appointments():
    
        return render_template("appointments/myappointments.html",
        user_reservations = Appointment.query.join(User.appointments).filter(User.id == current_user.id).order_by(Appointment.start_time.asc()).all())

    #return render_template("appointments/myappointments.html", user_reservations = Appointment.query.order_by(Appointment.start_time.asc()).all())

# Creating an appointment

@app.route("/appointments/new/", methods=["GET"])
@login_required(role="ADMIN")
def appointments_form():
    
    # If an user is trying to access the site through URL
    if current_user.employee is not True:
        return redirect(url_for("my_appointments"))

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
    def appointment_is_unique():
        appointmentTimes = Appointment.query.filter_by(start_time = form.time.data)

        for appointment in appointmentTimes:
            if appointment.accountappointment[0].id == current_user.id:
                return False

        return True 

    if not appointment_is_unique():
        form.time.errors.append("You have already an appointment at this starting time, please choose another time.")
        return render_template("appointments/new.html", form = form)

    new_appointment = Appointment(form.time.data)
    new_appointment.accountappointment.append(employee)  

    db.session().add(new_appointment)
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

    appointment = Appointment.query.get(appointment_id)

    db.session().delete(appointment)
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
    
    update_appointment = Appointment.query.get(appointment_id)
    
    # Populating the form fields with current information
    form = UpdateAppointmentForm(obj = update_appointment)

    employees = User.query.filter_by(employee = True)
    currentemployee = update_appointment.accountappointment[0]
    employeelist = [(currentemployee.id, currentemployee.name)]
    
    for employee in employees:
        if employee.id != currentemployee.id:
            employeelist.append([employee.id, employee.name])
    
    form.employees.choices = employeelist

    customers = User.query.filter_by(employee = False)
    services = Service.query.all()

    # If the appointment is reserved, populate first with current customer
    if update_appointment.reserved is True:
        currentcustomer = update_appointment.accountappointment[1]
        customerlist = [(currentcustomer.id, currentcustomer.name)]

        for customer in customers:
            if customer.id != currentcustomer.id:
                customerlist.append([customer.id, customer.name])

    else:
        customerlist = [(customer.id, customer.name) for customer in customers]

    # If there is a service connected to the appointment, populate it as first and fill the rest
    if len(update_appointment.services) > 0:
        currentservice = update_appointment.services[0]        
        serviceslist = [(currentservice.id, "".join(currentservice.service + ', ' + str(currentservice.price) + 'e'))]

        for service in services:
            if service.id != currentservice.id:
                serviceslist.append([service.id, "".join(service.service + ', ' + str(service.price) + 'e')])
    else:
        serviceslist = [(service.id, "".join(service.service + ', ' + str(service.price) + 'e')) for service in services]        

    form.users.choices = customerlist
    form.services.choices = serviceslist

    return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

@app.route("/appointments/update/commit/<appointment_id>/", methods=["POST"])
@login_required(role="ADMIN")
def appointments_updates(appointment_id):
    
    update_appointment = Appointment.query.get(appointment_id)
    form = UpdateAppointmentForm(request.form)
    
    employees = User.query.filter_by(employee = True)
    employeelist = [(employee.id, employee.name) for employee in employees]
    form.employees.choices = employeelist

    users = User.query.filter_by(employee = False)
    userslist = [(user.id, user.name) for user in users]
    form.users.choices = userslist
    
    services = Service.query.all()
    serviceslist = [(service.id, "".join(service.service + ', ' + str(service.price) + 'e')) for service in services]
    form.services.choices = serviceslist
    
    if not form.validate():
        render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    # If there are no services created and the employee is trying to update an appointment
    if len(serviceslist) < 1:
        form.services.errors.append("There are no services available. Please create a service.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)        

    # Only employee assigned to the appointment can update the appointment 
    if not update_appointment.accountappointment[0].id == current_user.id:
        form.employees.errors.append("You cannot update an appointment that you are not assigned to.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)
    
    currentYear = int(datetime.now().year)
    comparedYear = int(form.start_time.data.strftime('%Y'))

    # Checking if input year is smaller than current year or input year is more than two years ahead
    if currentYear > comparedYear or currentYear + 1 < comparedYear:
        form.start_time.errors.append("The time you picked is in the past or way too ahead in future, please choose another time.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    # Checking if chosen employee already has an appointment at this starting time (excluding the appointment that is being updated)
    def appointment_is_unique():
        appointmentTimes = Appointment.query.filter_by(start_time = form.start_time.data)

        for appointment in appointmentTimes:
            if appointment is not update_appointment and appointment.accountappointment[0].id == form.employees.data:
                return False

        return True 

    if not appointment_is_unique():
        form.employees.errors.append("Chosen employee already has an appointment time at this starting time, please choose another time.")
        return render_template("appointments/updateform.html", appointment = Appointment.query.get(appointment_id), form = form)

    # Updating the appointment
    user = User.query.get(form.users.data)
    employee = User.query.get(form.employees.data)
    service = Service.query.get(form.services.data)

    update_appointment.services.clear()
    update_appointment.accountappointment.clear()
    db.session().commit()

    update_appointment.start_time = form.start_time.data

    # If reserved is set to False, information about user and service are disregarded
    if form.reserved.data is False:
        update_appointment.accountappointment.append(employee)        
        update_appointment.reserved = form.reserved.data

        db.session().commit()        
        return redirect(url_for("appointments_updatelist"))
    
    update_appointment.accountappointment.append(employee)
    update_appointment.accountappointment.append(user)
    update_appointment.services.append(service)
    update_appointment.reserved = form.reserved.data

    db.session().commit()
  
    return redirect(url_for("appointments_updatelist"))

# Reserving an appointment

@app.route("/appointments/reserve/", methods=["GET"])
@login_required(role="ANY")
def appointments_reserve():
    
    # If an employee is trying to access the reserve site through URL
    if current_user.employee is True:
        return redirect(url_for("appointments_index"))

    form = ReserveServiceForm(request.form)

    services = Service.query.all()
    serviceslist = [(service.id, "".join(service.service + ', ' + str(service.price) + 'e')) for service in services]
    form.services.choices = serviceslist

    return render_template("appointments/reserve.html", 
        appointments = Appointment.query.filter_by(reserved = False).order_by(Appointment.start_time.asc()).all(), form = form)

@app.route("/appointments/reserve/<appointment_id>/", methods=["POST"])
@login_required(role="ANY")
def appointment_set_reserved(appointment_id):

    form = ReserveServiceForm(request.form)

    services = Service.query.all()
    serviceslist = [(service.id, service.service) for service in services]
    form.services.choices = serviceslist    

    if not form.validate():
        return render_template("appointments/reserve.html", 
        appointments = Appointment.query.filter_by(reserved = False).order_by(Appointment.start_time.asc()).all(), form = form) 

    appointment = Appointment.query.get(appointment_id)
    employee = appointment.accountappointment[0]
    appointment.accountappointment.clear()
    db.session().commit()    

    new_user = User.query.get(current_user.id)

    service_id = form.services.data
    new_service = Service.query.get(service_id)
    
    appointment.reserved = True
    appointment.services.append(new_service)
    appointment.accountappointment.append(employee) 
    appointment.accountappointment.append(new_user)        

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

    appointment = Appointment.query.get(appointment_id)

    employee = appointment.accountappointment[0]
    
    appointment.reserved = False
    appointment.accountappointment.clear()
    appointment.services.clear()
    db.session().commit()

    appointment.accountappointment.append(employee)

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