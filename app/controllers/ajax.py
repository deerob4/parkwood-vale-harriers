from flask import Blueprint, render_template
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
    return 'Ready et waiting!'