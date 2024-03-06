from sqlalchemy import select
from ..models import Map
from ..schemas import MapSchema
from flask import Blueprint, request, flash, jsonify
from flask_login import current_user, login_required
from ..extensions import db
import logging
import json

# Logging adapted from https://docs.python.org/3/howto/logging.html and https://realpython.com/python-logging/ and https://betterstack.com/community/guides/logging/json-logging/

maps = Blueprint('maps', __name__)

map_list_schema = MapSchema(many=True)
map_schema = MapSchema()


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
        flash('An error occurred while getting your maps. Please refresh the page to try again.')
        return 'An error occurred while getting maps', 500


@maps.post('/maps')
@login_required
def save_map():
    try:
        # Create a new map with the form data
        logging.info(f'Attempting to save map for user {current_user.id}')
        data = json.loads(request.get_json())

        new_map = Map(
            user_id=current_user.id,
            name=data['name'],
            data=data['data']
        )

        # Add the new map to the database
        db.session.add(new_map)
        db.session.commit()

        # Return the map and use the map_schema to serialize the map into JSON
        flash('Map Saved Successfully!')
        logging.info(f'Map for user {current_user.id} has been saved')
        return map_schema.dump(new_map), 201

    except Exception as e:
        logging.error(f'An error occurred while saving map for user {current_user.id}: {e}')
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
            return 'Map not found', 404

        # Check if the map belongs to the logged in user
        if map_to_delete.user_id != current_user.id:
            logging.error(f'Map with id {id} does not belong to user {current_user.id}')
            return 'You do not own this map', 401

        # Delete the map
        db.session.delete(map_to_delete)
        db.session.commit()

        logging.info(f'Map with id {id} deleted successfully')
        return 'Map Deleted Successfully!', 200

    except Exception as e:
        logging.error(f'An error occurred while deleting map with id {id}: {e}')
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
            return 'Map not found', 404

        # Check if the map belongs to the logged in user
        if map_to_retrieve.user_id != current_user.id:
            logging.error(f'Map with id {id} does not belong to user {current_user.id}')
            return 'You do not own this map', 401

        # Use the map_schema to serialize the map into JSON
        result = map_schema.dump(map_to_retrieve)

        logging.info(f'Map with id {id} retrieved successfully')
        return jsonify(result), 200

    except Exception as e:
        logging.error(f'An error occurred while retrieving map with id {id}: {e}')
        return 'An error occurred', 500


@maps.put('/maps/<int:id>')
@login_required
def insert_or_update_map(id):
    try:
        logging.info(f'Attempting to update map with id {id} for user {current_user.id}')
        # Query the database for the map to be updated
        map_to_update = db.session.scalar(select(Map).filter_by(id=id))

        data = json.loads(request.get_json())

        # Check if the map exists
        if map_to_update is None:
            # If it doesn't exist, create a new map
            logging.info(f'Map with id {id} not found, creating map')
            new_map = Map(
                id=id,
                user_id=current_user.id,
                name=data['name'],
                data=data['data']
            )

            # Add the new map to the database
            db.session.add(new_map)
            db.session.commit()
            return map_schema.dump(new_map), 201

        # If the map exists, check the map belongs to the logged in user
        if map_to_update.user_id != current_user.id:
            logging.error(f'Map with id {id} does not belong to user {current_user.id}')
            return 'You do not own this map', 401

        # Update the map
        map_to_update.name = data['name']
        map_to_update.data = data['data']

        # Commit the changes to the database
        db.session.commit()

        logging.info(f'Map with id {id} updated successfully')
        return jsonify({'message': 'Map updated successfully!',
                        'updated_map': map_schema.dump(map_to_update)
                        }), 200

    except Exception as e:
        logging.error(f'An error occurred while updating map with id {id}: {e}')
        return 'An error occurred', 500
