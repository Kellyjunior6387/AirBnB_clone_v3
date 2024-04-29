#!/usr/bin/python3
"""
View for amenity objects to handle all restful actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """Return a list of states """
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        all_amenities = list(amenity.to_dict() for amenity in amenities)
        return jsonify(all_amenities)
    elif request.method == 'POST':
        my_dict = request.get_json()
        if not my_dict:
            abort(400, "Not a JSON")
        if "name" not in my_dict.keys():
            abort(400, "Missing name")
        new_amenity = Amenity(**my_dict)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Return a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
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
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
