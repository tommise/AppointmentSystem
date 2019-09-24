
from application import db
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

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)

    def __init__(self, start_time):
        self.start_time = start_time
        self.reserved = False