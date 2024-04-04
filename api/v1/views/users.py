#!/usr/bin/python3
"""
A view for User object that handles all default RESTful
API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from models import storage
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
""" Methods to allow all users endpoints """


@app_views.route('/users', methods=ALLOWED_METHODS)
@app_views.route('/users/<user_id>', methods=ALLOWED_METHODS)
def handle_amenities(user_id):
    """The method handler for the user endpoint"""
    method_handler = {
        'GET': (get_user, get_all_users),
        'DELETE': remove_user,
        'POST': add_user,
        'PUT': update_user,
    }
    if request.method in method_handler:
        return method_handler[request.method](user_id)
    else:
        raise MethodNotAllowed(list(method_handler.keys()))


def get_all_users():
    all_users = storage.all(User).values()
    user_dict = []
    for user in all_users:
        user_dict = user.to_dict()
        user_dict.append(user_dict)
    return jsonify(user_dict)


def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        raise NotFound()
    return jsonify(user.to_dict())


def remove_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        raise NotFound()
    user.delete()
    storage.save()
    return jsonify({})


def add_user():
    """ Create a new user object """
    data = request.get_json()
    if not data:
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


def update_user(user_id):
    user = storage.get(User, user_id)
    if user in None:
        raise NotFound()
    data = request.get_json()
    if not data:
        raise BadRequest(description='Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
