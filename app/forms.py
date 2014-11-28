import datetime
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, DateField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from wtforms_components import DateRange

from datetime import *


def calculate_age(born):
#     born = datetime.date(born)
    today = date.today()
    print('shoot me down, lord.')
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class MemberForm(Form):
    name = StringField("What is your name?", validators=[DataRequired('You must enter your name.'), Regexp('^[A-Za-z" "]*$', message='Your name must only contain letters.')])
    dob = DateField("What is your date of birth?", validators=[DataRequired('You must enter your date of birth.')])
    email = StringField("What is your email?",
                        validators=[DataRequired('You must enter your email.'), Email('You must enter a valid email.')])
    password = PasswordField("Enter a password:", validators=[DataRequired('You must enter a password.'),
                                                              Length(8, 20,
                                                                     'Your password must be between 8-20 characters.')])
    confirm = PasswordField("Confirm your password:", validators=[DataRequired('You must confirm your password.'),
                                                                  EqualTo('password', 'Your passwords must match.')])
    charity_event = BooleanField("I want the chance to run in the charity event")
    distance = SelectField('What is the maximum distance you have run before?',
                           choices=[('l1', 'Less than 1 mile'), ('1-5', '1 - 5 miles'), ('6-10', '6 - 10 miles'),
                                    ('11-15', '11 - 15 miles'), ('16-20', '16 - 20 miles'),
                                    ('g20', 'More than 20 miles')])
    submit = SubmitField('Submit')
    
    def validate_distance(self, field):
        charity_event = self.charity_event
        if field.data == 'l1' and charity_event.data == True:
            raise ValidationError('You must be physically fit to run in the charity event.')
            
    def validate_dob(self, field):
        age = calculate_age(field.data)
        if age < 18:
            raise ValidationError('You must 18 or over to join.')
        if age > 75:
            raise ValidationError('You must be younger than 75 to join.')
            
            
            