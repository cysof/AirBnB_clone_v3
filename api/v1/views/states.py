#!/usr/bin/python3
"""Contain the state view for API"""

from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models.state import State
from models import storage

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""Methods allowed for the states endpoints"""


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    """The method handler for the states endpoint"""
    method_handler = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in method_handler:
        return method_handler[request.method](state_id)
    else:
        raise MethodNotAllowed(list(method_handler.keys()))


def get_states(state_id=None):
    """Get the state with a given ID or all state"""
    all_states = storage.all(State).values()
    if state_id:
        res = list(filter(lambda x: x.id == state_id, all_states))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


def remove_state(state_id=None):
    """Removes a state with a given id"""
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    """Add a new state"""
    data = request.get_json()
    if not data:
        raise BadRequest(description='Missing JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id=None):
    """updating the state API using id"""
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        data = request.get_json()
        if not data:
            raise BadRequest(description='Missing JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
