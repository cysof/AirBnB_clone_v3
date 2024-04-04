#!/usr/bin/python3
"""
A view for Amenity object that handles all default RESTful
API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models.amenity import Amenity
from models import storage
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
""" Methods to allow all amenities endpoints """


@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenities_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenities_id):
    """The method handler for the states endpoint"""
    method_handler = {
        'GET': (get_amenity, get_all_amenities),
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in method_handler:
        return method_handler[request.method](amenities_id)
    else:
        raise MethodNotAllowed(list(method_handler.keys()))


def get_all_amenities():
    """ List all amenities """
    all_amenities = storage.all(Amenity).values()
    amenity_dict = []
    for amenity in all_amenities:
        amenity_dict = amenity.to_dict()
        amenity_dict.append(amenity_dict)
    return jsonify(amenity_dict)


def get_amenity(amenity_id):
    """ Get amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        raise NotFound()
    return jsonify(amenity.to_dict)


def remove_amenity(amenity_id):
    """ Delete amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        raise NotFound()
    amenity.delete()
    storage.save()
    return jsonify({})


def add_amenity():
    """ Create a new amenity object """
    # amenity = storage.get(Amenity, amenity_id)
    # if amenity is None:
    #     raise NotFound()
    data = request.get_json()
    if not data:
        raise BadRequest(description='Missing JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')

    new_amenity = Amenity(**data)
    # new_amenity.amenity_id = amenity_id
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


def update_amenity(amenity_id):
    """ Edit properties of an existing object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        raise NotFound()
    data = request.get_json()
    if not data:
        raise BadRequest(description='Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict())
