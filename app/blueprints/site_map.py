from flask import Blueprint, url_for, current_app

site_map_blueprint = Blueprint('site-map', __name__)


# Adapted from https://stackoverflow.com/questions/13317536/get-list-of-all-routes-defined-in-the-flask-app/13318415#13318415

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@site_map_blueprint.route('/')
def site_map():
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if 'GET' in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return links
