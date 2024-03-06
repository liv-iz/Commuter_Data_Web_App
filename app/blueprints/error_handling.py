from flask import Blueprint, render_template

error_handling = Blueprint('error_handling', __name__)


@error_handling.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
