from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    dob = db.Column(db.Date)
    date_joined = db.Column(db.Date)
    distance = db.Column(db.String)
    charity_event = db.Column(db.Boolean)
    
    def __init__(self, id, name, email, dob, password, distance, date_joined, charity_event):
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.distance = distance
        self.date_joined = date_joined
        self.charity_event = charity_event
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return '<User: %r>' % self.id
    