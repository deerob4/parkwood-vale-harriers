from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Defines the user table and the fields.

    Each variable represents an individual field
    for the database, pertaining to the data collected
    in app.forms.MemberForm. The data type is also declared.
    All fields are of variable length. There is a one-to-many
    relationship between users and activities.
    """
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    dob = db.Column(db.Date)
    phone = db.Column(db.String)
    weight = db.Column(db.Integer)
    distance = db.Column(db.String)
    joined = db.Column(db.Date)
    charity_event = db.Column(db.Boolean)

    activities = db.RelationshipProperty('Activity', backref='user', lazy='dynamic')

    # Initialises the class to allow it to be referenced in helper functions.
    def __init__(self, name, username, email, dob, password, distance, charity_event, weight, phone, joined):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.dob = dob
        self.distance = distance
        self.charity_event = charity_event
        self.phone = phone
        self.weight = weight

    # Ensures the password is accessible.
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    # Encrypts the password and assigns it to the class variable.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks the entered password against the decrypted password hash.
    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

    # Returns the id of the current user.
    def get_id(self):
        return self.id

    # Obligatory identification function.
    def __repr__(self):
        return '<User: %r>' % self.id


class Activity(db.Model):
    """Defines the activities table and the fields.

    Each variable represents an individual field
    for the database, pertaining to the data collected
    in app.static.js.main. The data type is also declared.
    A foreign key is established between the user table,
    with users.id acting as the key; this creates a
    one-to-one link between the two tables (one user can
    have multiple activities.
    """
    __tablename__ = 'Activities'
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(8))
    effigy = db.Column(db.String)
    date = db.Column(db.Date)
    start = db.Column(db.String)
    finish = db.Column(db.String)
    hours = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    opinion = db.Column(db.String)
    thoughts = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    # Initialises the class to allow it to be referenced in helper functions.
    def __init__(self, sport, effigy, date, start, finish, calories, opinion, thoughts, hours, user_id):
        self.sport = sport
        self.effigy = effigy
        self.date = date
        self.start = start
        self.finish = finish
        self.hours = hours
        self.calories = calories
        self.opinion = opinion
        self.thoughts = thoughts
        self.user_id = user_id

    # Obligatory identification function.
    def __repr__(self):
        return '<Activity: %r (%r)>' % (self.id, self.sport)