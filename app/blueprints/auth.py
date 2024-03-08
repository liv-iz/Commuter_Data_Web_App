from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select, exc
from ..models import User
from ..extensions import db, bcrypt, login_manager
import logging

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.scalar(select(User).filter_by(id=user_id))


# Adapted from https://stackoverflow.com/a/36284881

@login_manager.unauthorized_handler
def handle_needs_login():
    flash('You have to be logged in to access this page.')
    return redirect(url_for('auth.login', next=request.endpoint))


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except Exception:
        return redirect(fallback)
    return redirect(dest_url)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        logging.info('Signup POST request received')
        try:
            # Get the user's details from the form
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email_address = request.form.get('email_address')
            occupation = request.form.get('occupation')
            password = request.form.get('password')
            logging.info(f'Attempting to create account for user with email: {email_address}')

            # If this returns a user, then the email already exists in database
            user: User | None = db.session.scalar(select(User).filter_by(email_address=email_address))
            if user:
                logging.info(f'Account creation failed because an account with this email address: {email_address} already exists')
                flash('An account with this email address already exists')
                return 'An account with this email address already exists', 400

            # Create a new user with the form data. Hash the password so the plaintext version isn't saved.
            logging.info(f'User with email: {email_address} is being added to database')
            new_user = User(
                email_address=email_address,
                first_name=first_name,
                last_name=last_name,
                occupation=occupation,
                password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
                maps=[]
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            logging.info(f'User with email: {email_address} has been added to database')
            return redirect(url_for('auth.login'))

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f'An error occurred while creating the account for user with {email_address} : {e}')
            flash('An error occurred while creating your account. Please try again.')
            return 'An error occurred while creating the account', 500

    logging.info('Signup GET request received')
    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logging.info('Login POST request received')

        # Get the user's email and password from the login form
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        logging.info(f'Trying to authenticate user with email: {email_address}')

        # Check if user actually exists and take password, hash it, and compare it to the hashed password in database using bcrypt
        user: User | None = db.session.scalar(select(User).filter_by(email_address=email_address))
        if not user or not bcrypt.check_password_hash(user.password_hash, str(password)):
            flash('Email or password is incorrect')
            # If user doesn't exist or password is wrong, reload the page
            return redirect(url_for('auth.login'), flash_message=True)

        logging.info(f'Authentication successful for user {user.id}')

        # If the above check passes, redirect user to profile page
        login_user(user, remember=remember)
        return redirect_dest(fallback=url_for('general.get_profile'))

    logging.info('Login GET request received')
    if current_user.is_authenticated:
        return redirect(url_for('general.get_profile'))
    return render_template('login.html')


@auth.route('/logout')
def logout():
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        logging.info(f'User {current_user.id} is attempting to log out')
        logout_user()
        # TODO: In CW2, change this to redirect to index page and flash message saying logged out successfully
        logging.info(f'User {current_user.id} logged out')
        return redirect(url_for('auth.login'))

    except Exception as e:
        logging.error(f'Error occurred while logging out user {current_user.id}: {e}')
        flash('An error occurred while logging out. Please try again.')
        return redirect(url_for('general.get_profile'))  # Redirect to profile page if error occurs


@auth.delete('/delete-user')
@login_required
def delete_user():
    try:
        user_id = current_user.id
        logging.info(f'User {user_id} is deleting their account')
        db.session.delete(current_user)
        db.session.commit()
        logging.info(f'User {user_id} deleted their account')

        logout_user()
        logging.info(f'User {user_id} logged out after successfully deleting account')
        return redirect(url_for('general.get_index'))

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f'Error occurred while deleting user {current_user.id}: {e}')
        flash('An error occurred while deleting your account. Please try again.')
        return redirect(url_for('general.get_profile'))  # Redirect to profile page if error occurs
