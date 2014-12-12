from flask import Blueprint, render_template, flash
from app.forms import MemberForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = MemberForm()
    if form.validate_on_submit():
        print('woohoo')
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('auth/register.html', form=form)