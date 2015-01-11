from flask import Blueprint
ajax = Blueprint('ajax', __name__)


@ajax.route('/swimming-block')
def swimming_block():
    return 