from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, DateField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class MemberForm(Form):
    name = StringField("What is your name?", validators=[DataRequired('You must enter your name.')])
    dob = DateField("What is your date of birth?", validators=[DataRequired('You must enter your date of birth.')])
    email = StringField("What is your email?",
                        validators=[DataRequired('You must enter your email.'), Email('You must enter a valid email.')])
    password = PasswordField("Enter a password:", validators=[DataRequired('You must enter a password.'),
                                                              Length(8, 20,
                                                                     'Your password must be between 8-20 characters.')])
    confirm = PasswordField("Confirm your password:", validators=[DataRequired('You must confirm your password.'),
                                                                  EqualTo('password', 'Your passwords must match.')])
    charity_event = BooleanField("Do you want to be in the team?")
    distance = SelectField('What is the maximum distance you have run before?',
                           choices=[('l1', 'Less than 1 mile'), ('1-5', '1 - 5 miles'), ('6-10', '6 - 10 miles'),
                                    ('11-15', '11 - 15 miles'), ('16-20', '16 - 20 miles'),
                                    ('g20', 'More than 20 miles')])
    submit = SubmitField('Submit')