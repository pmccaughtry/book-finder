import os
import sys
import requests
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from unittest.mock import patch, Mock

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "OK"})

    def test_catch_all(self):
        response = self.client.get("/non-existent-path")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "OK"})

    @patch('requests.get')
    def test_search_books_success(self, mock_get):
        # Mock successful API response
        mock_response = {
            "items": [
                {"id": "123", "volumeInfo": {"title": "Test Book"}}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.post(
            "/books",
            json={"terms": "python programming"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response["items"])

    @patch('requests.get')
    def test_search_books_with_plus(self, mock_get):
        # Test URL encoding when terms contain plus signs
        mock_response = {"items": []}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.post(
            "/books",
            json={"terms": "python+programming"}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_search_books_api_error(self, mock_get):
        # Mock API error response
        mock_get.return_value.status_code = 404

        response = self.client.post(
            "/books",
            json={"terms": "python programming"}
        )

        self.assertEqual(response.json(), {
            "status": "Error",
            "code": 404,
            "message": "Failed to fetch data from Google Books API"
        })

    @patch('requests.get')
    def test_search_books_json_decode_error(self, mock_get):
        # Mock JSON decode error
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = requests.exceptions.JSONDecodeError(
            "Invalid JSON", "", 0
        )

        response = self.client.post(
            "/books",
            json={"terms": "python programming"}
        )

        self.assertEqual(response.json(), {
            "status": "Error",
            "code": 500,
            "message": "Failed to decode JSON response"
        })

if __name__ == '__main__':
    unittest.main()

