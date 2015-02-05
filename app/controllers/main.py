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


@main.route('/profiles/<username>', methods=['GET', 'POST'])
@login_required
def profiles(username):
    possible_user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == possible_user.username:
        activity_number = len(Activity.query.filter_by(user_id=current_user.get_id()).all())
        total_users = len(User.query.all())
        name = ChangeName()
        email = ChangeEmail()
        phone = ChangePhone()
        weight = ChangeWeight()
        dob = ChangeDob()

        def modify_user(element):
            user = User.query.filter_by(id=current_user.get_id())
            user.element = element.field.data
            db.session.add(user)
            db.session.commit()
            flash('Your %s was was updated!', 'success' % element)
            return redirect(url_for('main.profiles'))

        if name.validate_on_submit():
            modify_user(name)
        if email.validate_on_submit():
            modify_user(email)
        if phone.validate_on_submit():
            modify_user(phone)
        if weight.validate_on_submit():
            modify_user(weight)
        if dob.validate_on_submit():
            modify_user(dob)

        return render_template('profiles/own_profile.html', current_user=current_user, activity_number=activity_number,
                               total_users=total_users, new_name=name, new_email=email, new_phone=phone,
                               new_weight=weight, new_dob=dob)
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