from application import db

# Creating a many-to-many *-* relationship table between service and appointment

service_appointment = db.Table("serviceappointment",
    db.Column("service_id", db.Integer, db.ForeignKey("service.id")),
    db.Column("appointment_id", db.Integer, db.ForeignKey("appointment.id")))

class Service(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(144), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    serviceappointment = db.relationship("Appointment", secondary = service_appointment, 
        lazy="subquery", backref = db.backref("services", lazy = True))

    #appointments = db.relationship("Appointment", backref='service.id', lazy=True)   
    
    def __init__(self, service, price):
        self.service = service
        self.price = price