from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, DateField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError, NumberRange

from app.models import User
from app.helpers import calculate_age


class MemberForm(Form):
    """Contains the fields and validators for the new member form."""

    name = StringField("What is your name?", 
           validators=[DataRequired('You must enter your name.'), 
           Regexp(r'^[A-Za-z\-" "]*$', 
           message='Your name may only contain letters.')])

    dob = DateField("What is your date of birth?", 
          validators=[DataRequired('You must enter your date of birth.')])

    email = StringField("What is your email?", 
            validators=[DataRequired('You must enter your email.'), 
            Email('You must enter a valid email.')])

    password = PasswordField("Enter a password:", 
               validators=[DataRequired('You must enter a password.'), 
               Length(8, 20, 'Your password must be 8 - 20 characters.')])

    confirm = PasswordField("Confirm your password:", 
              validators=[DataRequired('You must confirm your password.'), 
              EqualTo('password', 'Your passwords must match.')])

    charity_event = BooleanField("I want the chance to run in the charity event")

    distance = SelectField('What is the maximum distance you have run in the past year?', 
               choices=[('l1', 'Less than 1 mile'), 
                        ('1-5', '1 - 5 miles'), 
                        ('6-10', '6 - 10 miles'), 
                        ('11-15', '11 - 15 miles'), 
                        ('16-20', '16 - 20 miles'), 
                        ('g20', 'More than 20 miles')])

    weight = IntegerField('How much do you weigh in kg?', 
             validators=[DataRequired('You must enter your weight.'), 
             NumberRange(10, 100, 'Your weight must be between 10kg - 100kg.')])

    phone = StringField('What is your phone number?', 
            validators=[DataRequired('You must enter your phone number.'),
            Regexp(r'^\s*\(?(020[78]\)? ?[1-9][0-9]{2} ?[0-9]{4})|(0[1-8][0-9]{3}\)? ?[1-9][0-9]{2} ?[0-9]{3})\s*$', 
            message='You must enter a valid UK phone number.')])

    submit = SubmitField('Submit')


    def validate_distance(self, field):
        """Ensures the user has not ticked the charity event and is a poor runner."""
        charity_event = self.charity_event
        if field.data == 'l1' and charity_event.data is True:
            raise ValidationError('You must be physically fit to run in the charity event.')


    def validate_dob(self, field):
        """Ensures the user is between 18 - 75 years old."""
        age = calculate_age(field.data)
        if not 18 <= age <= 75:
            raise ValidationError('You must be 18 - 75 years old to join.')


    def validate_email(self, field):
        """Ensures the email address is unique"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('That email address has already been registered.')


class LoginForm(Form):
    """Contains the fields and validators for the login form."""
    email = StringField('What is your email?',
            validators=[DataRequired('You must enter your email.'), 
            Email('You must enter a valid email.')])

    password = PasswordField('What is your password?', 
               validators=[DataRequired('You must enter your password.')])

    remember = BooleanField('Remember me')
    
    login = SubmitField('Login')
