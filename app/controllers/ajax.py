from datetime import datetime
from math import ceil
from calendar import month_name

from flask import Blueprint, render_template, request, jsonify
from flask.ext.login import current_user

from app.models import Activity, db
from app.performance_data import performance_data


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

    The base values were arrived at by dividing each value provided by the
    board by 80. The formula takes the correct base value, and multiplies it
    by the weight of the user. This is then multiplied by
    the number of hours. This value is modified based on how well the activity went -
    each of the five options is assigned a value from -10 to 10; this is then
    added to the total value to arrive at the final number of calories.
    """
    base_calories = {
        'swimming': {'Backstroke': 5.1625, 'Breaststroke': 7.375, 'Butterfly': 8.1125, 'Freestyle (slow)': 5.1625,
                     'Freestyle (fast)': 7.375},
        'running': {'5 mph': 5.9, '6 mph': 7.375, '7 mph': 8.4875, '8 mph': 9.9625, '9 mph': 11.0625, '10 mph': 11.8},
        'cycling': {'Leisurely': 2.95, 'Gently': 4.425, 'Moderately': 5.9, 'Vigorously': 6.125, 'Very fast': 8.85,
                    'Racing': 11.8},
        'modifiers': {'Brilliant': 10, 'Pretty good': 5, 'About average': 0, 'Okay': -5, 'Awful': -10}
    }
    sport = request.json['sport'].lower()
    effigy = request.json['effigy']
    hours = request.json['hours']
    start = request.json['start']
    finish = request.json['finish']
    thoughts = request.json['thoughts']
    rating = request.json['rating']

    base_value = base_calories[sport][effigy]
    calories = (base_value * current_user.weight) * hours
    modifier = base_calories['modifiers'][rating]
    calories += modifier

    activity_data = {'calories': str(ceil(calories)), 'sport': sport, 'hours': hours, 'effigy': effigy,
                     'start': start, 'finish': finish, 'rating': rating, 'thoughts': thoughts}

    return jsonify(activity_data)


@ajax.route('/ajax/running', methods=['POST'])
def running():
    runs = Activity.query.filter_by(user_id=current_user.get_id(), sport='running').all()
    running_data = {'calories': [run.calories for run in runs if run.date.month == 3],
                    'dates': [run.date.strftime('%d %b') for run in runs if run.date.month == 3]}
    print(running_data)
    return jsonify(running_data=running_data)


@ajax.route('/ajax/performance', methods=['POST'])
def ajax_performance():
    month = request.get_data().decode("utf-8").lower()
    user_data = performance_data(month)
    return jsonify(user_data=user_data)