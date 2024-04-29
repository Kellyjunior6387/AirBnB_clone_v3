#!/usr/bin/python3
"""
View for review objects to handle all restful actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_reviews(place_id):
    """ Return a list of reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        reviews = place.reviews
        reviews = list(review.to_dict() for review in reviews)
        return jsonify(reviews)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if 'text' not in data:
            abort(400, "Missing text")
        if 'user_id' not in data:
            abort(400, "Missing user_id")
        user = storage.get(User, data['user_id'])
        if not user:
            abort(4004)
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review(review_id):
    """Return a Place object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
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
        data.pop('place_id', None)
        for key, value in data.items():
            setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
