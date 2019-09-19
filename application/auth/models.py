from application import db

class User(db.Model):

    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    employee = db.Column(db.Boolean, nullable=False)

    appointments = db.relationship("Appointment", backref='account', lazy=True)

    '''
    def __init__(self, name):
        self.name = name
    '''
    
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