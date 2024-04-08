from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
import logging
from sqlalchemy import select

from app.models import Map
from app.extensions import db

general = Blueprint('general', __name__)


@general.get('/')
def get_index():
    try:
        logging.info('GET request received at /')
        return render_template('index.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the index page: {e}')
        flash('An error occurred while accessing the index page. Please try again.', 'warning')
        return redirect(url_for('general.get_index'))


@general.get('/profile')
@login_required
def get_profile():
    try:
        logging.info('GET request received at /profile')
        return render_template('profile.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the profile: {e}')
        flash('An error occurred while accessing the profile. Please try again.', 'warning')
        return redirect(url_for('general.get_index'))  # Try to go to profile page again if error occurs


@general.get('/my_maps')
@login_required
def get_my_maps():
    try:
        # Query the database for all maps that belong to the logged in user
        logging.info(f'Attempting to collect user {current_user.id} maps')
        maps = db.session.scalars(select(Map).filter_by(user_id=current_user.id))

        logging.info('GET request received at /my_maps')
        return render_template('my_maps.html', maps=maps)
    except Exception as e:
        logging.error(f'An error occurred while accessing my maps: {e}')
        flash('An error occurred while accessing my maps. Please try again.', 'warning')
        return redirect(url_for('general.get_index'))


@general.get('/test')
def get_test():
    try:
        logging.info('GET request received at /test')
        flash('Welcome to the test page!', 'success')
        return render_template('test.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the test page: {e}')
        flash('An error occurred while accessing the test page. Please try again.', 'warning')
        return redirect(url_for('general.get_test'))


@general.get('/dynamic_map')
def get_dynamic_map():
    try:
        logging.info('GET request received at /dynamic_map')
        return render_template('dynamic_map.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the dynamic graph page: {e}')
        flash('An error occurred while accessing the dynamic graph page. Please try again.', 'warning')
        return redirect(url_for('general.get_index'))


@general.get('/data')
def get_data_page():
    try:
        logging.info('GET request received at /data')
        return render_template('data.html')
    except Exception as e:
        logging.error(f'An error occurred while accessing the data page: {e}')
        flash('An error occurred while accessing the data page. Please try again.', 'warning')
        return redirect(url_for('general.get_index'))
