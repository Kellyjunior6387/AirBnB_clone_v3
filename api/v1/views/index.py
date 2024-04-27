#!/usr/bin/python3
"""
Show status of api
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    retrieves the number of each objects by type
    """
    object_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(object_count)
