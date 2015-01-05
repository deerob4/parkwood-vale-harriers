from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, DateField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError

from datetime import date


def calculate_age(born):
    """Calculates the age of the user

    This function takes a date object provided
    by the user (in 'dob) and then operates it
    in comparison with the current date, working
    out the age of the user; this is returned as an int.
    """
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class MemberForm(Form):
    """Contains the fields and validators for the new member form."""

    name = StringField("What is your name?", validators=[DataRequired('You must enter your name.'),
                                                         Regexp('^[A-Za-z" "]*$',
                                                                message='Your name must only contain letters.')])
    dob = DateField("What is your date of birth?", validators=[DataRequired('You must enter your date of birth.')])
    email = StringField("What is your email?",
                        validators=[DataRequired('You must enter your email.'), Email('You must enter a valid email.')])
    password = PasswordField("Enter a password:", validators=[DataRequired('You must enter a password.'),
                                                              Length(8, 20,
                                                                     'Your password must be 8 - 20 characters.')])
    confirm = PasswordField("Confirm your password:", validators=[DataRequired('You must confirm your password.'),
                                                                  EqualTo('password', 'Your passwords must match.')])
    charity_event = BooleanField("I want the chance to run in the charity event")
    distance = SelectField('What is the maximum distance you have run in the last year?',
                           choices=[('l1', 'Less than 1 mile'), ('1-5', '1 - 5 miles'), ('6-10', '6 - 10 miles'),
                                    ('11-15', '11 - 15 miles'), ('16-20', '16 - 20 miles'),
                                    ('g20', 'More than 20 miles')])
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
            raise ValidationError('You must be 18 - 75 years old to join. %s years' % age)

            
class AddSwimForm(Form):
    """Contains the fields and validators for the new swim session form"""
    style = SelectField('Which style did you use?', choices=[('backstroke', 'Backstroke'), ('breaststroke', 'Breaststroke'), ('butterfly', 'Butterfly'), ('freestyle-slow', 'Freestyle (slow)'), ('freestyle-fast', 'Freestyle (fast)')])
    start = StringField('What time did you start?', validators=[DataRequired('You must enter your start time.')])
    finish = StringField('What time did you finish?', validators=[DataRequired('You must enter your finish time.')])
    rating = SelectField('How would you rate your swim?', choices=[('brilliant', 'Brilliant'), ('pretty-good', 'Pretty good'), ('about-average', 'About average'),('okay', 'Okay'), ('poor', 'Poor')])
    thoughts = TextAreaField('Do you have any extra thoughts?')
    submit = SubmitField('Add Swim')
