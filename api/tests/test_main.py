import os
import sys
import psutil
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

    @patch('psutil.cpu_count')
    @patch('psutil.cpu_percent')
    @patch('psutil.getloadavg')
    @patch('psutil.virtual_memory')
    @patch('psutil.boot_time')
    def test_health_details_success(self, mock_boot_time, mock_virtual_memory,
                                  mock_getloadavg, mock_cpu_percent, mock_cpu_count):
        # Set up mock returns
        mock_cpu_count.return_value = 8
        mock_cpu_percent.return_value = 35.2
        mock_getloadavg.return_value = (1.5, 1.7, 1.9)

        mock_memory = Mock()
        mock_memory.total = 16888888888  # About 16GB
        mock_memory.available = 8444444444
        mock_memory.used = 7444444444
        mock_memory.free = 1000000000
        mock_memory.percent = 45.7
        mock_virtual_memory.return_value = mock_memory

        mock_boot_time.return_value = 1704067200  # Example timestamp

        response = self.client.get("/health-details")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Verify CPU information
        self.assertEqual(data['cpu']['count'], 8)
        self.assertEqual(data['cpu']['percent'], 35.2)
        self.assertEqual(data['cpu']['loadavg']['1min'], 1.5)
        self.assertEqual(data['cpu']['loadavg']['5min'], 1.7)
        self.assertEqual(data['cpu']['loadavg']['15min'], 1.9)

        # Verify memory information
        self.assertEqual(data['memory']['percent'], 45.7)
        self.assertIsInstance(data['memory']['total'], float)
        self.assertIsInstance(data['memory']['available'], float)
        self.assertIsInstance(data['memory']['used'], float)
        self.assertIsInstance(data['memory']['free'], float)

        # Verify memory conversions (GB)
        self.assertAlmostEqual(data['memory']['total'], 15.73, places=1)
        self.assertAlmostEqual(data['memory']['available'], 7.86, places=1)
        self.assertAlmostEqual(data['memory']['used'], 6.93, places=1)
        self.assertAlmostEqual(data['memory']['free'], 0.93, places=1)

        # Verify uptime is returned as a float
        self.assertIsInstance(data['uptime'], float)

    @patch('psutil.cpu_count')
    def test_health_details_error(self, mock_cpu_count):
        # Mock an error in psutil
        mock_cpu_count.side_effect = Exception("Test error")

        response = self.client.get("/health-details")

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn('detail', data)
        self.assertIn('Test error', data['detail'])

    @patch('psutil.cpu_count')
    @patch('psutil.cpu_percent')
    @patch('psutil.getloadavg')
    @patch('psutil.virtual_memory')
    @patch('psutil.boot_time')
    def test_health_details_zero_values(self, mock_boot_time, mock_virtual_memory,
                                      mock_getloadavg, mock_cpu_percent, mock_cpu_count):
        # Test with zero or minimal values
        mock_cpu_count.return_value = 1
        mock_cpu_percent.return_value = 0.0
        mock_getloadavg.return_value = (0.0, 0.0, 0.0)

        mock_memory = Mock()
        mock_memory.total = 1024 * 1024  # 1MB
        mock_memory.available = 1024 * 1024
        mock_memory.used = 0
        mock_memory.free = 1024 * 1024
        mock_memory.percent = 0.0
        mock_virtual_memory.return_value = mock_memory

        mock_boot_time.return_value = datetime.now().timestamp()

        response = self.client.get("/health-details")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Verify minimal values are handled correctly
        self.assertEqual(data['cpu']['count'], 1)
        self.assertEqual(data['cpu']['percent'], 0.0)
        self.assertEqual(data['cpu']['loadavg']['1min'], 0.0)
        self.assertEqual(data['memory']['percent'], 0.0)
        self.assertGreater(data['memory']['total'], 0)

if __name__ == '__main__':
    unittest.main()

