#!/usr/bin/python3
"""
View for amenity objects to handle all restful actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Return a list of users """
    if request.method == 'GET':
        users = storage.all(User).values()
        all_users = list(user.to_dict() for user in users)
        return jsonify(all_users)
    elif request.method == 'POST':
        my_dict = request.get_json()
        if not my_dict:
            abort(400, "Not a JSON")
        if "email" not in my_dict:
            abort(400, "Missing email")
        if "password" not in my_dict:
            abort(400, "Missing password")
        new_user = User(**my_dict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """ Return a Amenity object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('email', None)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
