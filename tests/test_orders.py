import unittest, requests, uuid
from httmock import HTTMock
from models.orders import Order
from .mock import MockOrder

BASE_URL  = 'http://127.0.0.1:5000/api/v1/orders'

class OrderTest(unittest.TestCase):

    def setUp(self):
        self.mock_data = MockOrder()

    def test_get_orders(self):
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_order(self):
        test_data =  {
            "client_id": str(uuid.uuid4()),
            "location": "Bukoto",
            "menu_id": str(uuid.uuid4()),
            "quantity": 2
        }
        response = requests.post(BASE_URL, json=test_data)
        self.assertEqual(response.status_code, 201)
    
    def test_get_specific_order(self):
        """Mock data and then retrieve it."""
        with HTTMock(self.mock_data.mock_order_response):
            r = requests.get(BASE_URL + "/f262b0b6-be59-11e8-9e8b-e24b8e248ee6")
            self.assertEqual(r.status_code, 200)
            assert r.json()['quantity'] == 2
            assert r.json()['location'] == "Bukoto"
            assert r.json()['status'] == "pending"

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
        response = requests.put(BASE_URL + "/83f40d36-bdb0-11e8-9747-c01885e11dd7", data=status)
        self.assertEqual(response.status_code, 200)

    def test_update_specific_order_not_found(self):
        """Test for updating order not found."""
        status = {
            "status": "completed"
        }
        response = requests.put(BASE_URL + "/b3c6a8f4-bdb3-11e8-9747", json=status)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('error'), "Unable to find this order")

    def tearDown(self):
        self.mock_data = ""