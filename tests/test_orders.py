import unittest
import uuid
import requests
from httmock import HTTMock
from .mock import MockOrder

BASE_URL = 'https://manzede-fast-food-fast.herokuapp.com/api/v1/orders'

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
            "client_id": str(uuid.uuid4()),
            "location": "Bukoto",
            "menu_id": str(uuid.uuid4()),
            "quantity": 2
        }
        response = requests.post(BASE_URL, json=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('data')['location'], "Bukoto")
    def test_get_specific_order(self):
        """Mock data and then retrieve it."""
        with HTTMock(self.mock_data.mock_order_response):
            response = requests.get(BASE_URL + "/f262b0b6-be59-11e8-9e8b-e24b8e248ee6")
            self.assertEqual(response.status_code, 200)
            assert response.json()['quantity'] == 2
            assert response.json()['location'] == "Bukoto"
            assert response.json()['status'] == "completed"

    def test_get_specific_order_not_found(self):
        """Test specific order not found."""
        response = requests.get(BASE_URL + "/b6b7a7f8-0a1d-402d-b41a-03705debdb10")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('message'), "Cannot find this order")

    def test_update_specific_order(self):
        """Test update specific order."""
        status = {
            "status": "completed"
        } 
        with HTTMock(self.mock_data.mock_order_response):
            response = requests.put(BASE_URL + "/f262b0b6-be59-11e8-9e8b-e24b8e248ee6", json=status)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('status'), "completed")

    def test_update_specific_order_not_found(self):
        """Test for updating order not found."""
        status = {
            "status": "completed"
        }
        response = requests.put(BASE_URL + "/b3c6a8f4-bdb3-11e8-9747", json=status)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('error'), "Unable to find this order")

    def tearDown(self):
        """Destroy variable mock_data."""
        self.mock_data = ""
