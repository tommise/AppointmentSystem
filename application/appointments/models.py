
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

    #service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)

    def __init__(self, start_time):
        self.start_time = start_time
        self.reserved = False

    @staticmethod
    def get_reservations_by_id(id):
 
        stmt = text("SELECT Appointment.start_time, Account.username FROM Account"
                    " LEFT JOIN AccountAppointment ON AccountAppointment.account_id = account.id"
                    " LEFT JOIN Appointment ON AccountAppointment.appointment_id = appointment.id"
                    " WHERE Account.id = :uid;").params(uid = id)                   

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"start_time":row[0], "username":row[1]})
 
        return response        