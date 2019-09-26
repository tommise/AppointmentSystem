from application import db
from sqlalchemy.sql import text
from flask_login import current_user

class User(db.Model):

    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    employee = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, username, password, employee):
        self.name = name
        self.username = username
        self.password = password
        self.employee = employee
  
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True   

    def get_role(self):
        if self.employee is True:
            return "ADMIN"
        elif self.employee is False:
            return "USER"     

    @staticmethod
    def get_users_without_reservation():
 
        stmt = text("SELECT Account.name, Account.username FROM Account"
                    " LEFT JOIN AccountAppointment ON AccountAppointment.account_id = account.id"
                    " LEFT JOIN Appointment ON AccountAppointment.appointment_id = appointment.id"
                    " WHERE Account.employee = FALSE"
                    " GROUP BY account.name, account.username"
                    " HAVING COUNT(Appointment.id) = 0;")

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"name":row[0], "username":row[1]})
 
        return response 

    @staticmethod
    def get_all_employees():
 
        stmt = text("SELECT Account.name, Account.id FROM Account"
                    " WHERE Account.employee = TRUE"
                    " ORDER BY Account.id;")

        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"name":row[0]})
 
        return response
                   