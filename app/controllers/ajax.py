from flask import Blueprint, render_template, json, request, redirect, url_for, flash
from flask.ext.login import current_user, logout_user
from app.models import User, Activity, db

from datetime import datetime
from math import ceil

ajax = Blueprint('ajax', __name__)


# Defines the route for displaying the activity blocks
@ajax.route('/ajax/sport-block', methods=['POST'])
def sport_block():
    sport = request.get_data().decode("utf-8")
    if sport == 'running':
        return render_template('training/running_block.html')
    elif sport == 'cycling':
        return render_template('training/cycling_block.html')
    elif sport == 'swimming':
        return render_template('training/swimming_block.html')
    else:
        return '%s was passed as a sport - no template is available for this.' % sport, 400


# Defines the route for uploading activity block data
@ajax.route('/ajax/send-activity', methods=['POST'])
def send_activity():
    sport = request.json['sport']
    effigy = request.json['effigy']
    calories = request.json['calories']
    hours = request.json['hours']
    start = request.json['start']
    finish = request.json['finish']
    opinion = request.json['rating']
    thoughts = request.json['thoughts']

    activity = Activity(sport=sport, effigy=effigy, calories=calories, hours=hours, start=start,
                        finish=finish, opinion=opinion, thoughts=thoughts,
                        user_id=current_user.get_id(), date=datetime.now().date())

    db.session.add(activity)
    db.session.commit()
    print('Successfully saved Activity %s (%s) to the database.' % (activity.id, activity.sport))
    return 'success', 200


@ajax.route('/ajax/remove-activity', methods=['POST'])
def remove_activity():
    activity_id = request.json['activityId']
    Activity.query.filter_by(id=activity_id).delete()
    db.session.commit()
    print('Activity deleted.')
    return 'Activity deleted.', 200


@ajax.route('/ajax/calculate-calories', methods=['POST'])
def calculate_calories():
    """Calculates the number of calories burned in a session

    The base values for each type of training were arrived at
    by dividing each value provided by the board by 80. From here,
    total calories for other weights can be worked out. The
    algorithm works by taking the correct base value, and multiplying
    it by the weight of the user. This value is then multiplied by
    the number of hours spent on the activity. Finally, this value
    is modified based on how well the activity went - each of the
    five options is assigned a value from -10 to 10; this is then
    added to the total value to arrive at the final number of calories.
    """
    base_calories = {
        'swimming': {'backstroke': 5.1625, 'breaststroke': 7.375, 'butterfly': 8.1125, 'freestyle-slow': 5.1625,
                     'freestyle-fast': 7.375},
        'running': {'5mph': 5.9, '6mph': 7.375, '7mph': 8.4875, '8mph': 9.9625, '9mph': 11.0625, '10mph': 11.8},
        'cycling': {'leisure': 2.95, 'gentle': 4.425, 'moderate': 5.9, 'vigorous': 6.125, 'very-fast': 8.85,
                    'racing': 11.8},
        'modifiers': {'brilliant': 10, 'pretty-good': 5, 'average': 0, 'okay': -5, 'awful': -10}
    }
    sport = request.json['sport'].lower()
    effigy = request.json['effigy']
    hours = request.json['hours']
    rating = request.json['rating']

    base_value = base_calories[sport][effigy]
    calories = (base_value * current_user.weight) * hours
    modifier = base_calories['modifiers'][rating]
    calories += modifier

    return str(ceil(calories))


@ajax.route('/ajax/delete-account', methods=['POST'])
def delete_account():
    user_id = current_user.get_id()
    logout_user()
    User.query.filter_by(id=user_id).delete()
    Activity.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    print('User #%s and their activities were deleted.' % user_id)
    flash('Your account was successfully deleted - sorry to see you go!', 'success')
    return 'deleted'