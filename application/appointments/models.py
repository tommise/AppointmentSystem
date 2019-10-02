
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
    def get_most_popular_services():
 
        stmt = text("SELECT Service.service, COUNT(Service.id) FROM Service"
                    " INNER JOIN ServiceAppointment ON ServiceAppointment.service_id = Service.id"
                    " INNER JOIN Appointment ON ServiceAppointment.appointment_id = Appointment.id"
                    " WHERE Appointment.reserved = TRUE"
                    " GROUP BY Service.service, Service.id"
                    " ORDER BY COUNT(Service.service) DESC;")

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"name":row[0], "count":row[1]})
 
        return response