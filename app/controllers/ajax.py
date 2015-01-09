from flask import Blueprint, render_template, flash, redirect, url_for

ajax = Blueprint('ajax', __name__)

@ajax.route('/swimming-block')
def swimming_block():
    return 