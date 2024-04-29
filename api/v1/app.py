#!/usr/bin/python3
"""
Endpoint to return status of api
"""

import os
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', 5000))


@app.teardown_appcontext
def teardown_db(exception):
    """ closes the storage on teardown"""
    storage.close()

cors = CORS(app, resources={r'/*': {'origins': host}})


@app.errorhandler(404)
def not_found(error):
    """ returns a 404 error in json format"""
    return make_response({"error": "Not found"}, 404)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
