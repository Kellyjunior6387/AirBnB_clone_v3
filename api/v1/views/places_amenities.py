#!/usr/bin/python3
"""
 link between Place objects and Amenity objects that handles
 all default RESTFul API action
 """

from os import environ
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if STORAGE_TYPE == 'db':
        amenities = place.amenities
    else:
        amenities = []
        for amenity_id in place.amenity_ids:
            amenities.append(storage.get(Amenity, amenity_id))
    amenities = list(amenity.to_dict() for amenity in amenities)
    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def link_or_unlink_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if request.method == 'DELETE':
        if STORAGE_TYPE == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            if amenity.id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.pop(amenity.id)
            storage.save()
            return jsonify({}), 200
    elif request.method == 'POST':
        if STORAGE_TYPE == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            if amenity.id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.push(amenity.id)
            storage.save()
            return jsonify(amenity.to_dict()), 201
