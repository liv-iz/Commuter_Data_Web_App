from sqlalchemy import select, text, func
from ..models import Map, LocalAuthority, Hours, TravelDistance, TravelMethod
from ..schemas import MapSchema, HoursSchema, TravelDistanceSchema, TravelMethodSchema
from flask import Blueprint, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required
from ..extensions import db
import logging
import json

# Logging adapted from https://docs.python.org/3/howto/logging.html and https://realpython.com/python-logging/ and https://betterstack.com/community/guides/logging/json-logging/

maps = Blueprint('maps', __name__)

map_list_schema = MapSchema(many=True)
map_schema = MapSchema()
hours_schema = HoursSchema(many=True)
travel_distance_schema = TravelDistanceSchema(many=True)
travel_method_schema = TravelMethodSchema(many=True)


@maps.get('/maps')
@login_required
def get_all_user_maps():
    try:
        # Query the database for all maps that belong to the logged in user
        logging.info(f'Attempting to collect user {current_user.id} maps')
        user_maps = db.session.scalars(select(Map).filter_by(user_id=current_user.id))

        # Use the map_schema to serialize the maps into JSON
        logging.info(f'Serializing map list for user {current_user.id} into JSON')
        result = map_list_schema.dump(user_maps)

        # Return the maps
        logging.info('List of user maps successfully serialised, returning')
        return result, 200

    except Exception as e:
        logging.error(f'Error occurred while returning maps for user {current_user.id}: {e}')
        flash('An error occurred while getting your maps. Please try again.', 'error')
        return 'An error occurred while getting maps', 500


@maps.post('/maps')
@login_required
def save_map():
    try:
        # Create a new map with the form data
        logging.info(f'Attempting to save map for user {current_user.id}')
        data = request.get_json()

        new_map = Map(
            user_id=current_user.id,
            name=data['name'],
            data_source=data['dataSource'],
            data_source_label=data['dataSourceLabel'],
            attribute=data['attribute'],
            attribute_label=data['attributeLabel'],
            year=data['year'],
            min_colour=data['minColour'],
            max_colour=data['maxColour']
        )

        # Add the new map to the database
        db.session.add(new_map)
        db.session.commit()

        # Redirect the user to a view of the new map
        flash('Map Saved Successfully!', 'success')
        logging.info(f'Map for user {current_user.id} has been saved')
        return redirect(url_for('general.get_dynamic_map') + f'?dataSource={new_map.data_source}&dataSourceLabel={new_map.data_source_label}attribute={new_map.attribute}&attributeLabel={new_map.attribute_label}&year={new_map.year}&minColour={new_map.min_colour}&maxColour={new_map.max_colour}'), 201

    except Exception as e:
        logging.error(f'An error occurred while saving map for user {current_user.id}: {e}')
        flash('An error occurred while saving your map. Please try again.', 'error')
        return 'An error occurred while saving the map', 500


@maps.delete('/maps/<int:id>')
@login_required
def delete_map(id):
    try:
        logging.info(f'Attempting to delete map with id {id} for user {current_user.id}')
        # Query the database for the map to be deleted
        map_to_delete = db.session.scalar(select(Map).filter_by(id=id))

        # Check if the map exists
        if map_to_delete is None:
            logging.error(f'Map with id {id} not found')
            flash('Map not found', 'error')
            return 'Map not found', 404

        # Check if the map belongs to the logged in user
        if map_to_delete.user_id != current_user.id:
            logging.error(f'Map with id {id} does not belong to user {current_user.id}')
            flash('You do not own this map', 'error')
            return 'You do not own this map', 401

        # Delete the map
        db.session.delete(map_to_delete)
        db.session.commit()

        logging.info(f'Map with id {id} deleted successfully')
        flash('Map Deleted Successfully!', 'success')
        return 'Map Deleted Successfully!', 200

    except Exception as e:
        logging.error(f'An error occurred while deleting map with id {id}: {e}')
        flash('An error occurred whilst trying to delete the map', 'error')
        return 'An error occurred whilst trying to delete the map', 500


@maps.get('/maps/<int:id>')
@login_required
def get_map(id):
    try:
        logging.info(f'Attempting to get map with id {id} for user {current_user.id}')
        # Query the database for the map to be retrieved
        map_to_retrieve = db.session.scalar(select(Map).filter_by(id=id))

        # Check if the map exists
        if map_to_retrieve is None:
            logging.error('Map with id {id} not found')
            flash('Map not found', 'error')
            return 'Map not found', 404

        # Check if the map belongs to the logged in user
        if map_to_retrieve.user_id != current_user.id:
            logging.error(f'Map with id {id} does not belong to user {current_user.id}')
            flash('You do not own this map', 'error')
            return 'You do not own this map', 401

        # Use the map_schema to serialize the map into JSON
        result = map_schema.dump(map_to_retrieve)

        logging.info(f'Map with id {id} retrieved successfully')
        return jsonify(result), 200

    except Exception as e:
        logging.error(f'An error occurred while retrieving map with id {id}: {e}')
        flash('An error occurred while retrieving the map', 'error')
        return 'An error occurred', 500


@maps.put('/maps/<int:id>')
@login_required
def insert_or_update_map(id):
    try:
        logging.info(f'Attempting to update map with id {id} for user {current_user.id}')
        # Query the database for the map to be updated
        map_to_update = db.session.scalar(select(Map).filter_by(id=id))

        data = request.get_json()

        # Check if the map exists
        if map_to_update is None:
            # If it doesn't exist, create a new map
            logging.info(f'Map with id {id} not found, creating map')
            new_map = Map(
                user_id=current_user.id,
                name=data['name'],
                data_source=data['dataSource'],
                data_source_label=data['dataSourceLabel'],
                attribute=data['attribute'],
                attribute_label=data['attributeLabel'],
                year=data['year'],
                min_colour=data['minColour'],
                max_colour=data['maxColour']
            )

            # Add the new map to the database
            db.session.add(new_map)
            db.session.commit()
            return map_schema.dump(new_map), 201

        # If the map exists, check the map belongs to the logged in user
        if map_to_update.user_id != current_user.id:
            logging.error(f'Map with id {id} does not belong to user {current_user.id}')
            flash('Map cannot be updated. You do not own this map.', 'error')
            return 'You do not own this map', 401

        # Update the map
        map_to_update.name = data['name']
        map_to_update.data_source = data['dataSource']
        map_to_update.data_source_label = data['dataSourceLabel']
        map_to_update.attribute = data['attribute']
        map_to_update.attribute_label = data['attributeLabel']
        map_to_update.year = data['year']
        map_to_update.min_colour = data['minColour']
        map_to_update.max_colour = data['maxColour']

        # Commit the changes to the database
        db.session.commit()

        logging.info(f'Map with id {id} updated successfully')
        flash('Map Updated Successfully!', 'success')
        return jsonify({'message': 'Map updated successfully!',
                        'updated_map': map_schema.dump(map_to_update)
                        }), 200

    except Exception as e:
        logging.error(f'An error occurred while updating map with id {id}: {e}')
        flash('An error occurred while updating the map', 'error')
        return 'An error occurred', 500

# Guidance from: https://stackoverflow.com/questions/47192428/what-is-the-difference-between-with-entities-and-load-only-in-sqlalchemy

# Used https://medium.com/@jesscsommer/survival-guide-for-flask-sqlalchemy-queries-e442bbaf9ad for guidance and https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html and https://docs.sqlalchemy.org/en/20/core/selectable.html and https://stackoverflow.com/questions/30784456/sqlalchemy-return-a-record-filtered-by-max-value-of-a-column


@maps.get('/travel_method/<int:year>')
def get_travel_method(year: int):
    if year != 2021 and year != 2011:
        return 'Invalid year', 400

    column = request.args.get('column')
    if column and column in TravelMethod.__table__.columns:
        additional_column = getattr(TravelMethod, column)
    else:
        additional_column = None

    results = db.session.execute(select(
        TravelMethod.local_authority_code,
        func.sum(additional_column).label(column)
    ).filter(
        TravelMethod.census_year == year
    ).group_by(
        TravelMethod.local_authority_code)
    ).all()

    return {
        "results": [
            (
                str(result.local_authority_code),
                str(getattr(result, column)) if additional_column else None
            ) for result in results
        ]
    }, 200


@maps.get('/travel_distance/<int:year>')
def get_travel_distance(year: int):
    if year != 2021 and year != 2011:
        return 'Invalid year', 400

    column = request.args.get('column')
    if column and column in TravelDistance.__table__.columns:
        additional_column = getattr(TravelDistance, column)
    else:
        additional_column = None

    results = db.session.execute(select(
        TravelDistance.local_authority_code,
        func.sum(additional_column).label(column),
        func.sum(TravelDistance.employed_residents).label("employed_residents")
    ).filter(
        TravelDistance.census_year == year
    ).group_by(
        TravelDistance.local_authority_code)
    ).all()

    return {
        "results": [
            (
                result.local_authority_code,
                getattr(result, column) if additional_column else None,
                result.employed_residents
            ) for result in results
        ]
    }, 200


@maps.get('/hours_worked/<int:year>')
def get_hours_worked(year: int):
    if year != 2021 and year != 2011:
        return 'Invalid year', 400

    column = request.args.get('column')
    if column and column in Hours.__table__.columns:
        additional_column = getattr(Hours, column)
    else:
        additional_column = None

    results = db.session.execute(select(
        Hours.local_authority_code,
        func.sum(additional_column).label(column)
    ).filter(
        Hours.census_year == year
    ).group_by(
        Hours.local_authority_code)
    ).all()

    return {
        "results": [
            (
                str(result.local_authority_code),
                str(getattr(result, column)) if additional_column else None
            ) for result in results
        ]
    }, 200


@maps.get('/local-authority-geometries')
def get_local_authority_geometries():
    try:
        local_authorities = db.session.scalars(select(LocalAuthority))

        return {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "local_authority_code": local_authority.code,
                        "local_authority_name": local_authority.name
                    },
                    "geometry": json.loads(local_authority.geometry)
                } for (i, local_authority) in enumerate(local_authorities)
            ]
        }, 200

    except Exception as e:
        logging.error(f'An error occurred while returning area data: {e}')
        flash('An error occurred while getting area data. Please try again.', 'error')
        return 'An error occurred while getting area data', 500


@maps.get('/most_used_travel_method/<int:year>')
def most_used_travel_method(year: int):
    if year != 2021 and year != 2011:
        return 'Invalid year', 400

    query_text = text(f"""
        SELECT local_authority_code,
            CASE
                WHEN work_from_home = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Work from home'
                WHEN underground = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Underground'
                WHEN train = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Train'
                WHEN bus = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Bus'
                WHEN taxi = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Taxi'
                WHEN motorcycle = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Motorcycle'
                WHEN car_driver = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Car driver'
                WHEN car_passenger = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Car passenger'
                WHEN bicycle = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Bicycle'
                WHEN walk = MAX(work_from_home, underground, train, bus, taxi, motorcycle, car_driver, car_passenger, bicycle, walk, other) THEN 'Walking'
                ELSE 'Other'
            END AS most_used_method
        FROM travel_method
        WHERE census_year = {year}
        GROUP BY local_authority_code
    """)
    query = db.session.execute(query_text)

    results = query.all()

    return {
        "results": [
            (
                str(result.local_authority_code),
                str(result.most_used_method)
            ) for result in results
        ]
    }, 200


@maps.get('/employed_residents_2021')
def employed_residents_2021():
    results = db.session.execute(select(
        TravelMethod.local_authority_code,
        func.sum(TravelMethod.employed_residents).label('employed_residents')
        ).filter(
            TravelMethod.census_year == 2021
        ).group_by(
            TravelMethod.local_authority_code)
        ).all()

    return {
        "data": [
            (
                str(result.local_authority_code),
                str(result.employed_residents)
            ) for result in results
        ]
    }, 200
