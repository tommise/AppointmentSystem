from application import db

class Service(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(144), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    appointments = db.relationship("Appointment", backref='service.id', lazy=True)   
    
    def __init__(self, service, price):
        self.service = service
        self.price = price