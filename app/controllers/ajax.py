from flask import Blueprint, render_template, json, request
from flask.ext.login import current_user
from app.models import Activity, db

from datetime import datetime

ajax = Blueprint('ajax', __name__)


def calculate_calorie_base():
    calories_per_hour = {
        'swimming': {
            'backstroke': 413,  # 5.1625
            'breaststroke': 590,  # 7.375
            'butterfly': 649,  # 8.1125
            'freestyle-slow': 413,  # 5.1625
            'freestyle-fast': 590  # 7.375
        },
        'running': {
            '5mph': 472,  # 5.9
            '6mph': 590,  # 7.375
            '7mph': 679,  # 8.4875
            '8mph': 797,  # 9.9625
            '9mph': 885,  # 11.0625
            '10mph': 944  # 11.8
        },
        'cycling': {
            'leisure': 236,  # 2.95
            'gentle': 354,  # 4.425
            'moderate': 472,  # 5.9
            'vigorous': 590,  # 6.125
            'very-fast': 708,  # 8.85
            'racing': 944  # 11.8
        }
    }


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
        return '%s was passed as a sport - no template is available for this.' % sport, 500


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

    return 'All is good down here'


@ajax.route('/ajax/remove-activity', methods=['POST'])
def remove_activity():
    activity_id = request.json['activityId']
    Activity.query.filter_by(id=activity_id).delete()
    db.session.commit()
    print('Activity deleted.')
    return 'Activity deleted.'