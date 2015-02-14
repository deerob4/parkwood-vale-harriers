from flask import flash, redirect, url_for
from flask.ext.login import current_user

from app.models import db

from datetime import date


def update_user(user, element, redirect_user=True):
    """Adds the updated user to the db and reloads the page."""
    db.session.add(user)
    db.session.commit()
    flash('Your %s has been successfully changed!' % element, 'success')
    if redirect_user:
        return redirect(url_for('main.profiles', username=user.username))


def validation_error(message):
    """Displays an appropriate error message and reloads the page."""
    flash(message, 'warning')
    return redirect(url_for('main.profiles', username=current_user.username))


def calculate_age(born):
    """Calculates the age of the user"""
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))