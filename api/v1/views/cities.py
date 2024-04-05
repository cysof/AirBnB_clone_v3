from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_cities(state_id=None, city_id=None):
    method_handler = {
        'GET': get_cities,
        'DELETE': remove_city,
        'POST': add_city,
        'PUT': update_city,
    }
    if request.method in method_handler:
        return method_handler[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(method_handler.keys()))

def get_cities(state_id=None, city_id=None):
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            raise NotFound("State not found")
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    elif city_id:
        city = storage.get(City, city_id)
        if not city:
            raise NotFound("City not found")
        return jsonify(city.to_dict())
    raise NotFound()

def remove_city(state_id=None, city_id=None):
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            raise NotFound("City not found")
        storage.delete(city)
        if storage_t != "db":
            for place in storage.all(Place).values():
                if place.city_id == city_id:
                    for review in storage.all(Review).values():
                        if review.place_id == place.id:
                            storage.delete(review)
                    storage.delete(place)
        storage.save()
        return jsonify({}), 200
    raise NotFound()

def add_city(state_id=None, city_id=None):
    state = storage.get(State, state_id)
    if not state:
        raise NotFound("State not found")
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Invalid JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name in JSON')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201

def update_city(state_id=None, city_id=None):
    xkeys = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            raise NotFound("City not found")
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description='Invalid JSON')
        for key, value in data.items():
            if key not in xkeys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    raise NotFound()
