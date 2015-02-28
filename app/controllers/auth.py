from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user, login_user, logout_user
from random import randint

from app.forms import MemberForm, LoginForm
from app.models import db, User


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated():
        form = MemberForm()
        if form.validate_on_submit():
            # Generates a username for the user composed of their real name and a random number
            username = form.name.data.lower().replace(' ', '') + str(randint(1, 10))
            user = User(name=form.name.data, username=username, email=form.email.data, password=form.password.data,
                        dob=form.dob.data, distance=form.distance.data, charity_event=form.charity_event.data,
                        phone=form.phone.data, weight=form.weight.data, joined=datetime.now())
            db.session.add(user)
            db.session.commit()
            print('%s has been registered.' % user.name)
            flash('You can now login!', 'success')
            return redirect(url_for('auth.login'))
        for error in form.errors.items():
            flash(error[1][0], 'warning')
        return render_template('auth/register.html', form=form)
    return redirect(url_for('main.home'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated():
        form = LoginForm()
        if form.validate_on_submit():
            # Query that returns the first user with the entered email address.
            user = User.query.filter_by(email=form.email.data).first()
            # Checks that a user was returned and that the password is correct.
            if user is not None and user.check_password(form.password.data):
                login_user(user, form.remember.data)
                return redirect(url_for('main.home'))
            flash('Invalid email address or password.', 'warning')
        for error in form.errors.items():
            flash(error[1][0], 'warning')
        return render_template('auth/login.html', form=form)
    return redirect(url_for('main.home'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))