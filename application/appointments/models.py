
from application import db
from sqlalchemy.sql import text
from datetime import datetime

# Creating a many-to-many *-* relationship table between account and appointment

account_appointment = db.Table("accountappointment",
    db.Column("account_id", db.Integer, db.ForeignKey("account.id")),
    db.Column("appointment_id", db.Integer, db.ForeignKey("appointment.id")))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    reserved = db.Column(db.Boolean, nullable=False)

    accountappointment = db.relationship("User", secondary = account_appointment, 
        lazy="subquery", backref = db.backref("appointments", lazy = True))

    def __init__(self, start_time):
        self.start_time = start_time
        self.reserved = False

    @staticmethod
    def get_reservations_by_id(user_id):
 
        stmt = text("SELECT Appointment.start_time, Account.username FROM Account"
                    " LEFT JOIN AccountAppointment ON AccountAppointment.account_id = account.id"
                    " LEFT JOIN Appointment ON AccountAppointment.appointment_id = appointment.id"
                    " WHERE Account.id = :uid"
                    " ORDER BY Appointment.start_time;").params(uid = user_id)                

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"start_time":row[0], "username":row[1]})
 
        return response

    @staticmethod
    def get_appointments():
 
        stmt = text("SELECT Appointment.id, Appointment.start_time, Account.name, Appointment.reserved FROM Account"
                    " LEFT JOIN AccountAppointment ON AccountAppointment.account_id = account.id"
                    " LEFT JOIN Appointment ON AccountAppointment.appointment_id = appointment.id"
                    " WHERE Account.employee = True AND Appointment.id IS NOT NULL"
                    " ORDER BY Appointment.start_time;")         

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"id":row[0], "start_time":row[1], "employee":row[2], "reserved":row[3]})
 
        return response
        
            