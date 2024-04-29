#!/usr/bin/python3
"""
View for place objects to handle all restful actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """ Return a list of places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        places = city.places
        places = list(place.to_dict() for place in places)
        return jsonify(places)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if 'name' not in data:
            abort(400, "Missing name")
        if 'user_id' not in data:
            abort(400, "Missing user_id")
        user = storage.get(User, data['user_id'])
        if not user:
            abort(4004)
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place(place_id):
    """Return a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('user_id', None)
        data.pop('city_id', None)
        for key, value in data.items():
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
