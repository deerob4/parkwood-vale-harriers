from flask import Blueprint, render_template, json, request
from app.models import Activity

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
    rating = request.json['rating']
    thoughts = request.json['thoughts']
    print('Rating: %s' % rating)
    return 'All is good down here'
    