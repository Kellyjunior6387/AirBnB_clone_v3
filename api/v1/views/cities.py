#!/usr/bin/python3
"""
View for city objects to handle all restful actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """ Return a list of cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        cities = state.cities
        cities = list(city.to_dict() for city in cities)
        return jsonify(cities)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if 'name' not in data:
            abort(400, "Missing name")
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city(city_id):
    """Return a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        for key, value in data.items():
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
