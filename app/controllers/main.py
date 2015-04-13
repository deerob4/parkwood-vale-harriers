from datetime import datetime
from calendar import month_name

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import current_user, login_required, logout_user
from flask.ext.sqlalchemy import *
import re

from app.models import User, Activity, db
from app.helpers import validation_error, update_user
from app.performance_data import performance_data

main = Blueprint('main', __name__)

current_date = datetime.now().date()


@main.route('/')
@login_required
def home():
    return redirect(url_for('main.performance', month='march'))


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
                validation_error('Your name may only contain letters and dashes.')

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
    """Returns add activity page; returns all the training sessions done on current day"""
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
    months = [month_name[x].lower() for x in range(1, 13)]
    all_activities = Activity.query.filter_by(user_id=current_user.get_id()).all()
    available_months = []

    # Calculates all the months that the user has done activities in
    for activity in all_activities:
        for x in range(1, 13):
            if activity.date.month == x and months[x - 1] not in available_months:
                available_months.append(months[x - 1])
    print(available_months)

    if month.lower() in available_months:
        user_data = performance_data(month.lower())
        return render_template('performance/user_performance.html', user_data=user_data,
                               current_month=month.title(), months=available_months)
    abort(404)


@main.route('/performance/compare', methods=['GET', 'POST'])
@login_required
def compare_performance():
    """Builds the dropdown list for comparison page"""
    users = User.query.filter_by(charity_event=0).filter(User.id != current_user.id).all()
    user_list = sorted([[user.id, user.name] for user in users])
    return render_template('/performance/compare_performance.html', users=users, user_list=user_list)


@main.route('/rankings')
@login_required
def rankings():
    """Calculates the best running team"""
    user_ranking = {}
    runners = User.query.filter_by(charity_event=False).all()
    for runner in runners:
        total_calories = 0
        training_sessions = Activity.query.filter_by(user_id=runner.id).all()
        for session in training_sessions:
            total_calories += session.calories
        user_ranking[runner.name] = total_calories

    user_ranking = sorted(user_ranking, key=user_ranking.get, reverse=True)
        
    return render_template('/training/rankings.html', running_team=user_ranking)


@main.errorhandler(404)
def page_not_found(error):
    """If page cannot be found, return custom error page"""
    return render_template('errors/404.html'), 404

