from flask import Blueprint, render_template, flash
from app.forms import MemberForm

from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = MemberForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.email.data, form.password.data, 
                    form.dob.data, datetime.now().date(), form.distance.data,
                    form.charity_event.data)
        db.session.add(user)
        db.session.commit()
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('auth/register.html', form=form)