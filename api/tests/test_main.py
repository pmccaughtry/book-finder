import os
import sys
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


if __name__ == '__main__':
    unittest.main()

