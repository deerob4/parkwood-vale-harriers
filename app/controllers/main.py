from datetime import datetime
from math import floor
from calendar import month_name

from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask.ext.login import current_user, login_required, logout_user
from random import randint
import re

from app.models import User, Activity, db
from app.helpers import validation_error, update_user


main = Blueprint('main', __name__)

current_date = datetime.now().date()


@main.route('/')
@login_required
def home():
    return redirect(url_for('main.user_performance'))


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


@main.route('/performance', methods=['GET'])
@login_required
def user_performance():
    return redirect(url_for('main.performance', month=current_date.strftime('%B').lower()))


@main.route('/performance/<month>', methods=['GET', 'POST'])
@login_required
def performance(month):
    months = [month_name[x].lower() for x in range(1, 13)]  # Constructs a list of month names
    if month in months:
        all_activities = Activity.query.filter_by(user_id=current_user.get_id()).all()
        all_runs = Activity.query.filter_by(user_id=current_user.get_id(), sport='running').all()
        all_cycles = Activity.query.filter_by(user_id=current_user.get_id(), sport='cycling').all()
        all_swims = Activity.query.filter_by(user_id=current_user.get_id(), sport='swimming').all()

        month_map = dict(zip(months, range(1, 13)))  # Creates a dict with month names and values - Jan: 1 etc

        print(months)
        print(month_map)

        calorie_goal = 62700
        hour_goal = 60

        # [0] contains the calories burned; [1] contains the hours
        total_run_data = [0, 0]
        total_cycle_data = [0, 0]
        total_swim_data = [0, 0]

        for run in all_runs:
            if run.date.month == month_map[month]:
                total_run_data[0] += run.calories
                total_run_data[1] += run.hours

        for cycle in all_cycles:
            if cycle.date.month == month_map[month]:
                total_cycle_data[0] += cycle.calories
                total_cycle_data[1] += cycle.hours

        for swim in all_swims:
            if swim.date.month == month_map[month]:
                total_swim_data[0] += swim.calories
                total_swim_data[1] += swim.hours

        user_data = {
            'progress_data': {
                'running': {
                    'calories': {
                        'value': total_run_data[0],
                        'percentage': total_run_data[0] / calorie_goal * 100
                    },
                    'hours': {
                        'value': total_run_data[1],
                        'percentage': total_run_data[1] / hour_goal * 100
                    }
                },
                'cycling': {
                    'calories': {
                        'value': total_cycle_data[0],
                        'percentage': total_cycle_data[0] / calorie_goal * 100
                    },
                    'hours': {
                        'value': total_cycle_data[1],
                        'percentage': total_cycle_data[1] / hour_goal * 100
                    }
                },
                'swimming': {
                    'calories': {
                        'value': total_swim_data[0],
                        'percentage': total_swim_data[0] / calorie_goal * 100
                    },
                    'hours': {
                        'value': total_swim_data[1],
                        'percentage': total_swim_data[1] / hour_goal * 100
                    }
                }
            },
            'sport_data': {
                'running': all_runs,
                'cycling': all_cycles,
                'swimming': all_swims
            }
        }

        # return render_template('performance/user_performance.html', user_data=user_data, month=month.title())
        return render_template('errors/404.html')
    abort(404)
