from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import MemberForm, LoginForm
from app.models import db, User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = MemberForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=form.password.data, dob=form.dob.data,
                    distance=form.distance.data, charity_event=form.charity_event.data)
        db.session.add(user)
        db.session.commit()
        print('%s has been registered.' % user.name)
        flash('You can now login!', 'success')
        return redirect(url_for('auth.login'))
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Query that returns the first user with the entered email address.
        user = User.query.filter_by(email=form.email.data).first()
        # Checks that a user was returned and that the password is correct.
        if user is not None and user.check_password(form.password.data):
            return redirect(url_for('main.home'))
        flash('Invalid email address or password.', 'warning')
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('auth/login.html', form=form)
