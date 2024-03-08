import os
from flask import Flask
from .extensions import db, ma, bcrypt, login_manager
from .config import DevConfig, ProdConfig, TestConfig
from .blueprints.auth import auth as auth_blueprint
from .blueprints.site_map import site_map_blueprint
from .blueprints.maps import maps as maps_blueprint
from .blueprints.general import general as general_blueprint
from .blueprints.error_handling import error_handling as error_handling_blueprint

# Adapted from https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/ and https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load the config for the current environment
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProdConfig)
    elif os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise flask extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(maps_blueprint, url_prefix='/api')
    app.register_blueprint(general_blueprint, url_prefix='/')
    if os.environ.get('FLASK_ENV') != 'production':
        app.register_blueprint(site_map_blueprint, url_prefix='/site-map')

    # Register error handlers
    app.register_blueprint(error_handling_blueprint)

    return app
