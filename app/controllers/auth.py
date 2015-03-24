from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user, login_user, logout_user
from random import randint

from app.forms import MemberForm, LoginForm
from app.models import db, User


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the register page and saves new users to the database"""
    # Makes sure logged in users cannot access the register page
    if not current_user.is_authenticated():
        form = MemberForm()
        # If the submit button is pressed
        if form.validate_on_submit():
            # Generates a username for the user composed of their real name and a random number
            username = form.name.data.lower().replace(' ', '') + str(randint(1, 10))
            # Creates a User object with the data they typed in
            user = User(name=form.name.data, username=username, email=form.email.data, password=form.password.data,
                        dob=form.dob.data, distance=form.distance.data, charity_event=form.charity_event.data,
                        phone=form.phone.data, weight=form.weight.data, joined=datetime.now())
            # Saves the user to the database
            db.session.add(user)
            db.session.commit()
            print('%s has been registered.' % user.name)
            # Returns the user to the login page with a message
            flash('You can now login!', 'success')
            return redirect(url_for('auth.login'))
        # If there were validation errors, re-render the view and show them
        for error in form.errors.items():
            flash(error[1][0], 'warning')
        return render_template('auth/register.html', form=form)
    return redirect(url_for('main.home'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page and logs in the user"""
    if not current_user.is_authenticated():
        form = LoginForm()
        if form.validate_on_submit():
            # Query that returns the first user with the entered email address.
            user = User.query.filter_by(email=form.email.data).first()
            # Checks that a user was returned and that the password is correct.
            if user is not None and user.check_password(form.password.data):
                # If so, log them in and redirect them to the home page
                login_user(user, form.remember.data)
                return redirect(url_for('main.home'))
            flash('Invalid email address or password.', 'warning')
        # If there were validation errors, re-render the view and show them
        for error in form.errors.items():
            flash(error[1][0], 'warning')
        return render_template('auth/login.html', form=form)
    return redirect(url_for('main.home'))


@auth.route('/logout')
def logout():
    """Logs the user out of the system"""
    logout_user()
    return redirect(url_for('main.home'))