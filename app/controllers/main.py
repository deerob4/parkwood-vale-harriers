from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask.ext.login import current_user, login_required

from app.forms import ChangeName, ChangeEmail, ChangePhone, ChangeDob, ChangeWeight
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


@main.route('/profiles/<username>')
@login_required
def profiles(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == user.username:
        activity_number = len(Activity.query.filter_by(user_id=current_user.get_id()).all())
        total_users = len(User.query.all())
        new_name = ChangeName()
        new_email = ChangeEmail()
        new_phone = ChangePhone()
        new_weight = ChangeWeight()
        new_dob = ChangeDob()
        if new_name.validate_on_submit():
            user = User.query.filter_by(id=current_user.get_id())
            user.name = new_name.name.data
            db.session.add(user)
            db.session.commit()
            flash('Your name was updated!', 'success')
            return redirect(url_for('main.profiles'))
        return render_template('profiles/own_profile.html', current_user=current_user, activity_number=activity_number,
                               total_users=total_users, new_name=new_name, new_email=new_email, new_phone=new_phone,
                               new_weight=new_weight, new_dob=new_dob)
    abort(403)


@main.route('/training/add', methods=['GET', 'POST'])
@login_required
def add_training():
    activities = Activity.query.filter_by(user_id=current_user.get_id(), date=current_date).all()
    total_calories = 0
    for activity in activities:
        total_calories += activity.calories
    return render_template('training/add_training.html', date=current_date,
                           current_user=current_user, activities=activities, total_calories=total_calories)