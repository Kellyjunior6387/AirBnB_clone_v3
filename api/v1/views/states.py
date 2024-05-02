#!/usr/bin/python3
"""
View for state obkects to handle all restful actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ Return a list of states """
    if request.method == 'GET':
        states = storage.all("State").values()
        all_states = []
        for state in states:
            all_states.append(state.to_dict())
        return jsonify(all_states)
    elif request.method == 'POST':
        my_dict = request.get_json()
        if not my_dict:
            abort(400, "Not a JSON")
        if "name" not in my_dict.keys():
            abort(400, "Missing name")
        new_state = State(**my_dict)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    """ Return a state object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
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
            setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
