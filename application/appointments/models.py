
from application import db
from datetime import datetime

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    reserved = db.Column(db.Boolean, nullable=False)
    
    # REMEMBER TO CREATE FOREIGN KEYS

    def __init__(self, start_time):
        self.start_time = start_time
        self.reserved = False