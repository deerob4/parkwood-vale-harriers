from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user, login_required

from app.forms import ChangeDetails
from app.models import User, Activity, db

from datetime import datetime

main = Blueprint('main', __name__)

current_date = datetime.now().date()


@main.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('main.add_training'))
    return redirect(url_for('auth.login'))


@main.route('/training/')
@login_required
def training():
    return 'All training will be here!'


@main.route('/runners/<runnername>')
@login_required
def runners(runnername):
    user = User.query.filter_by(username=runnername).first_or_404()
    if user.username == current_user.username:
        return render_template('profiles/own_profile.html', current_user=current_user)
    return 'no permissions...', 402


@main.route('/myprofile')
@login_required
def my_profile():
    return render_template('profiles/own_profile.html', current_user=current_user)


@main.route('/myprofile/edit', methods=['GET', 'POST'] )
@login_required
def edit_profile():
    form = ChangeDetails()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        user.name = form.name.data
        user.email = form.email.data
        user.dob = form.dob.data
        db.session.add(user)
        db.session.commit()
        flash('Your details have been updated!', 'success')
        return redirect(url_for('main.my_profile'))
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('profiles/change_details.html', current_user=current_user, form=form)


@main.route('/training/add', methods=['GET', 'POST'])
@login_required
def add_training():
    activities = Activity.query.filter_by(user_id=current_user.get_id(), date=current_date).all()
    return render_template('training/add_training.html', date=current_date,
                           current_user=current_user, activities=activities)