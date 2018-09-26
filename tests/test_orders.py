import unittest
import requests
import random
from httmock import HTTMock
from .mock import MockOrder

# BASE_URL = 'https://manzede-fast-food-fast.herokuapp.com/api/v1/orders'
BASE_URL = "http://127.0.0.1:5000/api/v1/orders"

class OrderTest(unittest.TestCase):
    """Order Tests."""

    def setUp(self):
        """Create an object of MockOrder."""
        self.mock_data = MockOrder()

    def test_get_orders(self):
        """Test get all orders."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get('orders'), list)

    def test_post_order(self):
        """Post new order."""
        test_data = {
            "client_id": random.randint(100,200),
            "location": "Bukoto",
            "menu_id": random.randint(300,400),
            "quantity": 2
        }
        response = requests.post(BASE_URL, json=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('data')['location'], "Bukoto")
    def test_get_specific_order(self):
        """Mock data and then retrieve it."""
        with HTTMock(self.mock_data.mock_order_response):
            response = requests.get(BASE_URL + "/12345")
            self.assertEqual(response.status_code, 200)
            assert response.json()['quantity'] == 2
            assert response.json()['location'] == "Bukoto"
            assert response.json()['status'] == "completed"

    def test_get_specific_order_not_found(self):
        """Test specific order not found."""
        response = requests.get(BASE_URL + "/98989")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('message'), "Cannot find this order")

    def test_update_specific_order(self):
        """Test update specific order."""
        status = {
            "status": "completed"
        } 
        with HTTMock(self.mock_data.mock_order_response):
            response = requests.put(BASE_URL + "/12345", json=status)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('status'), "completed")

    def test_update_specific_order_not_found(self):
        """Test for updating order not found."""
        status = {
            "status": "completed"
        }
        response = requests.put(BASE_URL + "/98989", json=status)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('error'), "Unable to find this order")

    def tearDown(self):
        """Destroy variable mock_data."""
        self.mock_data = ""
