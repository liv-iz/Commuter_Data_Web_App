from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
import logging

general = Blueprint('general', __name__)


@general.get('/profile')
@login_required
def get_profile():
    try:
        logging.info('GET request received at /profile')
        return render_template('profile.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the profile: {e}')
        flash('An error occurred while accessing the profile. Please try again.')
        return redirect(url_for('general.get_profile'))  # Try to go to profile page again if error occurs (TODO: maybe redirect to index page instead)


@general.get('/')
def get_index():
    try:
        logging.info('GET request received at /')
        return render_template('index.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the index page: {e}')
        flash('An error occurred while accessing the index page. Please try again.')
        return redirect(url_for('general.get_index'))
