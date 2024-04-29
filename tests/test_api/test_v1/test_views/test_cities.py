import json
import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from api.v1.views.cities import get_city

class TestCities(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    def test_get_city_success(self):
        with patch('api.v1.views.cities.storage.get') as mock_get:
            mock_city = {'id': 1, 'name': 'New York'}
            mock_get.return_value = mock_city
            response = self.client.get('/cities/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), mock_city)

    def test_get_city_not_found(self):
        with patch('api.v1.views.cities.storage.get') as mock_get:
            mock_get.return_value = None
            response = self.client.get('/cities/1')
            self.assertEqual(response.status_code, 404)

    def test_delete_city_success(self):
        with patch('api.v1.views.cities.storage.get') as mock_get, \
             patch('api.v1.views.cities.storage.delete') as mock_delete, \
             patch('api.v1.views.cities.storage.save') as mock_save:
            mock_city = {'id': 1, 'name': 'New York'}
            mock_get.return_value = mock_city
            response = self.client.delete('/cities/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {})

    def test_put_city_success(self):
        with patch('api.v1.views.cities.storage.get') as mock_get, \
             patch('api.v1.views.cities.request') as mock_request, \
             patch('api.v1.views.cities.jsonify') as mock_jsonify:
            mock_city = {'id': 1, 'name': 'New York'}
            mock_get.return_value = mock_city
            mock_request.method = 'PUT'
            mock_request.get_json.return_value = {'name': 'Los Angeles'}
            response = self.client.put('/cities/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {'id': 1, 'name': 'Los Angeles'})

if __name__ == '__main__':
    unittest.main()