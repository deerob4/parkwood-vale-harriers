from datetime import datetime
from calendar import month_name
from random import randint

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

        # If the user attempts to delete their account
        elif request.form.get('delete'):
            if request.form.get('delete') != 'I will lose everything':
                validation_error('You must type in the message exactly!')
            else:
                user_id = current_user.get_id()
                logout_user()
                User.query.filter_by(id=user_id).delete()  # Deletes the user's record
                Activity.query.filter_by(user_id=user_id).delete()  # Deletes all the user's activities
                db.session.commit()
                flash('Your account was successfully deleted - sorry to see you go!', 'success')
                return redirect(url_for('auth.login'))

    possible_user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == possible_user.username:
        activity_number = len(Activity.query.filter_by(user_id=current_user.get_id()).all())
        total_users = len(User.query.all())
        return render_template('profiles/own_profile.html', current_user=current_user, activity_number=activity_number, total_users=total_users)

    # If the user is not the profile they attempted to access, 403 
    abort(403)


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
    return render_template('training/add_training.html', date=current_date, current_user=current_user, activities=activities,
                           total_calories=total_calories, total_hours=total_hours)


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

    if month.lower() in available_months:
        user_data = performance_data(month.lower())
        return render_template('performance/user_performance.html', user_data=user_data,
                                current_month=month.title(), months=available_months)
    # If they haven't done any training in that month, 404
    abort(404)


@main.route('/performance/compare/<username>', methods=['GET', 'POST'])
@login_required
def compare_performance(username):
    """Builds the dropdown list for comparison page and returns the comparison data"""

    if User.query.filter_by(username=username).first():
        users = User.query.filter_by(charity_event=0).filter(User.id != current_user.id).all()
        user_list = sorted([[user.username, user.name] for user in users])
        comparison_id = User.query.filter_by(username=username).first().id
        comparison_name = User.query.filter_by(username=username).first().name.split(' ', 1)[0]

        # Creates a large dictionary with all the user's activities and the comparison's activities
        activities = {
            'runs': {
                'user': Activity.query.filter_by(user_id=current_user.get_id(), sport='running').all(),
                'comparison': Activity.query.filter_by(user_id=comparison_id, sport='running').all()
            },
            'cycles': {
                'user': Activity.query.filter_by(user_id=current_user.get_id(), sport='cycling').all(),
                'comparison': Activity.query.filter_by(user_id=comparison_id, sport='cycling').all()
            },
            'swims': {
                'user': Activity.query.filter_by(user_id=current_user.get_id(), sport='swimming').all(),
                'comparison': Activity.query.filter_by(user_id=comparison_id, sport='swimming').all()
            }
        }

        # Adds up all the user's running activities
        user_run_calories = 0
        user_run_hours = 0
        for run in activities['runs']['user']:
            user_run_calories += run.calories
            user_run_hours += run.hours

        # Adds up all the user's cycling activities
        user_cycle_calories = 0
        user_cycle_hours = 0
        for cycle in activities['cycles']['user']:
            user_cycle_calories += cycle.calories
            user_cycle_hours += cycle.hours

        # Adds up all the user's running activities
        user_swim_calories = 0
        user_swim_hours = 0
        for swim in activities['swims']['user']:
            user_swim_calories += swim.calories
            user_swim_hours += swim.hours

        user_calorie_total = user_run_calories + user_cycle_calories + user_swim_calories
        user_hour_total = user_run_hours + user_cycle_hours + user_swim_hours

        # Adds up all the comparison's running activities
        comparison_run_calories = 0
        comparison_run_hours = 0
        for run in activities['runs']['comparison']:
            comparison_run_calories += run.calories
            comparison_run_hours += run.hours

        # Adds up all the comparison's cycling activities
        comparison_cycle_calories = 0
        comparison_cycle_hours = 0
        for cycle in activities['cycles']['comparison']:
            comparison_cycle_calories += cycle.calories
            comparison_cycle_hours += cycle.hours

        # Adds up all the comparison's running activities
        comparison_swim_calories = 0
        comparison_swim_hours = 0
        for swim in activities['swims']['comparison']:
            comparison_swim_calories += swim.calories
            comparison_swim_hours += swim.hours

        # Adds up all the data
        comparison_calorie_total = comparison_run_calories + comparison_cycle_calories + comparison_swim_calories
        comparison_hour_total = comparison_run_hours + comparison_cycle_hours + comparison_swim_hours

        # Creates a big long dictionary which contains all the data for both the logged in and the comparison user
        user_data = {
            'user': {
                'calories': {
                    'running': user_run_calories, 'swimming': user_swim_calories, 'cycling': user_cycle_calories,
                    'total': user_calorie_total
                },
                'hours': {
                    'running': user_run_hours, 'swimming': user_swim_hours, 'cycling': user_cycle_hours,
                    'total': user_hour_total
                }
            },
            'comparison': {
                'calories': {
                    'running': comparison_run_calories, 'swimming': comparison_swim_calories, 'cycling': comparison_cycle_calories,
                    'total': comparison_calorie_total
                },
                'hours': {
                    'running': comparison_run_hours, 'swimming': comparison_swim_hours, 'cycling': comparison_cycle_hours,
                    'total': comparison_hour_total
                }
            }

        }

        return render_template('/performance/compare_performance.html', user_list=user_list,
                               activities=user_data, comparison_name=comparison_name)
    abort(404)


@main.route('/rankings')
@login_required
def rankings():
    """Calculates the best running team.

    The algorithm is not very advanced - it simply
    loops through all the runners who have opted into
    the charity event and then loops through all their
    activities, adding together all the calories. The
    runners are then sorted in order of who has the months
    calories.
    """
    user_ranking = {}
    runners = User.query.filter_by(charity_event=False).all()
    for runner in runners:
        user_calorie_total_calories = 0
        training_sessions = Activity.query.filter_by(user_id=runner.id).all()
        for session in training_sessions:
            user_calorie_total_calories += session.calories
        user_ranking[runner.name] = user_calorie_total_calories

    print(user_ranking)
    user_ranking = sorted(user_ranking, key=user_ranking.get, reverse=True)

    return render_template('/training/rankings.html', running_team=user_ranking)


@main.errorhandler(404)
def page_not_found(error):
    """If page cannot be found, return custom error page"""
    return render_template('errors/404.html'), 404

