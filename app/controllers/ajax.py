from flask import Blueprint, render_template, json, request
from flask.ext.login import current_user
from app.models import Activity, db

from datetime import datetime
from time import strptime

ajax = Blueprint('ajax', __name__)

# Defines the routes for displaying the activity blocks
@ajax.route('/ajax/swimming-block', methods=['POST'])
def swimming_block():
    return render_template('training/swimming_block.html')


@ajax.route('/ajax/running-block', methods=['POST'])
def running_block():
    return render_template('training/running_block.html')


@ajax.route('/ajax/cycling-block', methods=['POST'])
def cycling_block():
    return render_template('training/cycling_block.html')


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
    
    start = strptime(start, '%H:%M %p')
    finish = strptime(finish, '%H:%M %p')
    
    activity = Activity(sport=sport, effigy=effigy, calories=calories, hours=hours, start=start, 
                       finish=finish, opinion=opinion, thoughts=thoughts, 
                       user_id=current_user.get_id(), date=datetime.now().date())
    
    db.session.add(activity)
    db.session.commit()
    
    return 'All is good down here'
    