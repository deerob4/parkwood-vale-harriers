from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import MemberForm
from app.models import db, User

from datetime import datetime

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
        return redirect(url_for('main.home'))
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('auth/register.html', form=form)