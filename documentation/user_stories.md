# User Stories and SQL statements for the Appointment System

## User

#### Reserving a free appointment time

As an user, I am able to reserve an available time from a list and see the employees name who is connected to the appointment.

Listing all free appointment times:
```
SELECT * FROM Appointment WHERE Appointment.reserved = False;
```

Reserving an appointment time:
```
INSERT INTO AccountAppointment (appointment_id, account_id) VALUES (?, ?);
```
#### Listing appointments

As an user, I am able to list all my reserved appointment times.
```
SELECT Appointment.start_time, Appointment.reserved, Service.service FROM Appointment JOIN ServiceAppointment ON Appointment.service_id = Service.id JOIN AccountAppointment ON AccountAppointment.appointment_id = Appointment.id WHERE AccountAppointment.account_id = Account.id AND employee = True;
```

#### Canceling appointment

As an user, I am able to cancel an appointment I have reserved.
```
DELETE FROM AccountAppointment WHERE AccountAppointment.appointment_id = Appointment.id;
```

#### Signing up

As an user I am able to sign up for the site by providing my name, username and password.
```
INSERT INTO Account (name, username, password, employee) VALUES (?, ?, ?, False);
```

#### Logging in

As an user, I am able to log in to the site using my previously created username and password and log off the site.
```
SELECT Account.id, Account.name, Account.username, Account.password, Account.employee FROM Account WHERE Account.id = ?;
```
## Employee

### CRUD functionality for Appointments

#### Creating an appointment

As an employee, I am able to create a new appointment
```
INSERT INTO Appointment (start_time, reserved) VALUES (?, False);
```
#### Listing my appointments

As an employee, I am able to list my appointments
```
SELECT Appointment.start_time, Appointment.reserved, Service.service FROM Appointment JOIN ServiceAppointment ON ServiceAppointment.service_id = Service.id JOIN AccountAppointment ON AccountAppointment.appointment_id = Appointment.id WHERE AccountAppointment.id = Account.id AND employee = False;
```
#### Listing all appointments

As an employee, I am able to list all appointments
```
SELECT * FROM Appointment;
```
#### Update my appointment

As an employee, I am able to update my appointments
```
UPDATE Appointment SET Appointment.start_time = ?, Appointment.reserved WHERE Appointment.id = ?;
```
#### Removing my appointment

As an employee, I am able to remove my appointment
```
DELETE FROM Appointment WHERE Appointment.id = ?;
```

### CRUD functionality for Service

#### Creating a service

As an employee, I am able to create a new service
```
INSERT INTO Service (service, price) VALUES (?, ?);
```
#### Listing all services

As an employee, I am able to list all services
```
SELECT Service.service, service.price FROM Service;
```
#### Update services

As an employee, I am able to update all services
```
UPDATE Service SET Service.service = ?, Service.price WHERE Service.id = ?;
```

#### Removing a service

As an employee, I am able to remove all services
```
DELETE FROM Service WHERE Service.id = ?;
```

#### Logging in

As an employee, I am able to log in and off to the site using pre-made credentials.

```
SELECT Account.id, Account.name, Account.username, Account.password, Account.employee FROM Account WHERE Account.id = ?;
```

### Statistics

As an employee, I am able to list all users without an reservation
```
SELECT Service.service, COUNT(Service.id) FROM Service INNER JOIN ServiceAppointment ON ServiceAppointment.service_id = Service.id INNER JOIN Appointment ON ServiceAppointment.appointment_id = Appointment.id WHERE Appointment.reserved = True GROUP BY Service.service, Service.id ORDER BY COUNT(Service.id) DESC;
```

As an employee, I am able to list the most popular services
```
SELECT Account.name, Account.username FROM Account LEFT JOIN AccountAppointment ON AccountAppointment.account_id = account.id LEFT JOIN Appointment ON AccountAppointment.appointment_id = appointment.id WHERE Account.employee = False GROUP BY account.name, account.username HAVING COUNT(Appointment.id) = 0;
```
