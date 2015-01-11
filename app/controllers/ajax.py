from flask import Blueprint, render_template
ajax = Blueprint('ajax', __name__)


@ajax.route('/ajax/swimming-block', methods=['POST'])
def swimming_block():
    return render_template('training/swimming_block.html')


@ajax.route('/ajax/running-block', methods=['POST'])
def running_block():
    return '<p>Running is coming soon...</p>'


@ajax.route('/ajax/cycling-block', methods=['POST'])
def cycling_block():
    return '<p>Cycling is coming soon...</p>'