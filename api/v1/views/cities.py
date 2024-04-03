#!/usr/bin/python3
"""
A view for City object that handles all default RESTful
API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models.city import City
from models import storage
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""Methods to allow all cities endpoints"""


@app_views.route('/states/<state_id>/cities', methods=ALLOWED_METHODS)
@app_views.route('/cities/<city_id>', methods=ALLOWED_METHODS)
def handle_cities(city_id=None):
    """handler for cities endpoints"""
    method_handler = {
            'GET': (get_cities, get_city),
            'DELETE': remove_city,
            'POST': create_city,
            'PUT': update_city,
    }
    if request.method in method_handler:
        return method_handler[request.method](city_id)
    else:
        raise MethodNotAllowed(list(method_handler.keys()))


def get_cities(state_id):
    """ Gets list of cities from states_id"""
    state = storage.get(State, state_id)
    if state is None:
        raise NotFound()
    list_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(list_cities)


def get_city(city_id):
    """Get city by cities_id"""
    city = storage.get(City, city_id)
    if city is None:
        raise NotFound()
    return jsonify(city.to_dict())


def remove_city(city_id):
    """ Deletes city by city_id """
    city = storage.get(City, city_id)
    if city is None:
        raise NotFound()
    city.delete()
    storage.save()
    return jsonify({})


def create_city(states_id):
    """ Creates a city from states_id """
    state = storage.get(State, states_id)
    if state is None:
        raise NotFound()
    data = request.get_json()
    if not data:
        raise BadRequest(description='Missing JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')

    new_city = City(**data)
    new_city.state_id = states_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


def update_city(city_id):
    """ Edit and update a city object from city_id """
    city = storage.get(City, city_id)
    if city is None:
        raise NotFound()
    data = request.get_json()
    if not data:
        raise BadRequest(description='Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    storage.save()
    return jsonify(city.to_dict())
