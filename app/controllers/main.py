from datetime import datetime
from math import floor
from calendar import month_name

from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask.ext.login import current_user, login_required, logout_user
from random import randint
import re

from app.models import User, Activity, db
from app.helpers import validation_error, update_user
from app.performance_data import performance_data

main = Blueprint('main', __name__)

current_date = datetime.now().date()


@main.route('/')
@login_required
def home():
    return redirect(url_for('main.performance'))


@main.route('/profiles/<username>', methods=['GET', 'POST'])
@login_required
def profiles(username):
    # If the user has attempted to change their profile
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.get_id()).first()

        # If the user tries to change their name
        if request.form.get('name'):
            only_letters = re.compile(r'^[A-Za-z\-" "]*$')
            if only_letters.match(request.form.get('name')):
                user.name = request.form.get('name').title()
                user.username = request.form.get('name').lower().replace(' ', '').replace('-', '') + str(randint(1, 10))
                update_user(user, 'name', False)
                return redirect(url_for('main.profiles', username=user.username))
            else:
                validation_error('Your name may only contain letters.')

        # If the user tries to change their email
        elif request.form.get('email'):
            valid_email = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$')
            if valid_email.match(request.form.get('email')):
                user.email = request.form.get('email')
                update_user(user, 'email')
            else:
                validation_error('You must enter a valid email.')

        # If the user tries to change their phone number
        elif request.form.get('phone'):
            valid_phone = re.compile(
                r'^\s*\(?(020[78]\)? ?[1-9][0-9]{2} ?[0-9]{4})|(0[1-8][0-9]{3}\)? ?[1-9][0-9]{2} ?[0-9]{3})\s*$')
            if valid_phone.match(request.form.get('phone')):
                user.phone = request.form.get('phone')
                update_user(user, 'phone number')
            else:
                validation_error('You must enter a valid UK phone number.')

        # If the user tries to change their dob
        elif request.form.get('dob'):
            user.dob = request.form.get('dob')
            update_user(user, 'date of birth')

        # If the user tries to change their weight
        elif request.form.get('weight'):
            check_integer = re.compile(r'^-?[0-9]+$')
            if not check_integer.match(request.form.get('weight')):
                validation_error('You must enter a number.')
            elif not 10 <= int(request.form.get('weight')) <= 100:
                validation_error('Your weight must be between 10kg - 100kg.')
            else:
                user.weight = request.form.get('weight')
                update_user(user, 'weight')

        elif request.form.get('delete'):
            if request.form.get('delete') != 'I will lose everything':
                validation_error('You must type in the message exactly!')
            else:
                user_id = current_user.get_id()
                logout_user()
                User.query.filter_by(id=user_id).delete()
                Activity.query.filter_by(user_id=user_id).delete()
                db.session.commit()
                flash('Your account was successfully deleted - sorry to see you go!', 'success')
                return redirect(url_for('auth.login'))

    possible_user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == possible_user.username:
        activity_number = len(Activity.query.filter_by(user_id=current_user.get_id()).all())
        total_users = len(User.query.all())

        return render_template('profiles/own_profile.html', current_user=current_user, activity_number=activity_number,
                               total_users=total_users)
    abort(403)

    return redirect(url_for('main.profiles', username=current_user.username))


@main.route('/add-training', methods=['GET', 'POST'])
@login_required
def add_training():
    activities = Activity.query.filter_by(user_id=current_user.get_id(), date=current_date).all()
    total_calories = 0
    total_hours = 0
    for activity in activities:
        total_calories += activity.calories
        total_hours += activity.hours
    return render_template('training/add_training.html', date=current_date,
                           current_user=current_user, activities=activities, total_calories=total_calories,
                           total_hours=total_hours)


@main.route('/performance/<month>', methods=['GET', 'POST'])
@login_required
def performance(month):
    user_data = performance_data(month.lower())

    return render_template('performance/user_performance.html', user_data=user_data,
                           month=month.title())


@main.route('/performance/activity/<int:activity_id>')
@login_required
def individual_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first_or_404()
    return render_template('performance/individual_activity.html', activity=activity)


@main.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404