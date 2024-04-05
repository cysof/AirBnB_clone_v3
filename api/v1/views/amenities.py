from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/amenities', methods=ALLOWED_METHODS)
def handle_amenities():
    handlers = {
        'GET': get_amenities,
        'POST': add_amenity,
    }
    if request.method in handlers:
        return handlers[request.method]()
    else:
        raise MethodNotAllowed(list(handlers.keys()))


@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenity(amenity_id):
    handlers = {
        'GET': get_amenity,
        'DELETE': remove_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities():
    all_amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(amenities), 200


def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        raise NotFound("Amenity not found")


def remove_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        raise NotFound("Amenity not found")


def add_amenity():
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest("Invalid JSON data")
    if 'name' not in data:
        raise BadRequest("Missing 'name' in JSON data")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


def update_amenity(amenity_id):
    xkeys = ('id', 'created_at', 'updated_at')
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest("Invalid JSON data")
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        for key, value in data.items():
            if key not in xkeys:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        raise NotFound("Amenity not found")
