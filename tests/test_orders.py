import unittest, requests, uuid, datetime
from models.orders import Order

BASE_URL  = 'http://127.0.0.1:5000/api/v1/orders'

order = Order()
copy_data =  {
            "client_id": "274u83-473874-85845-4895596",
            "created_at": str(datetime.datetime.now()),
            "id": "83f40d36-bdb0-11e8-9747-c01885e11dd7",
            "location": "Bukoto",
            "menu_id": "28784933-2984938-1283933-394349",
            "quantity": 2,
            "status": "pending"
        }

class OrderTest(unittest.TestCase):

    def setUp(self):
        self.orders = order.orders.append(copy_data)

    def test_get_orders(self):
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_order(self):
        test_data =  {
            "client_id": str(uuid.uuid4()),
            "created_at": str(datetime.datetime.now()),
            "id": str(uuid.uuid1()),
            "location": "Bukoto",
            "menu_id": str(uuid.uuid4()),
            "quantity": 2,
            "status": "pending"
        }
        response = requests.post(BASE_URL, json=test_data)
        self.assertEqual(response.status_code, 201)
    
    def test_get_specific_order(self):
        response = requests.get(BASE_URL + "/b3c6a8f4-bdb3-11e8-9747-c01885e11dd7")
        self.assertEqual(response.status_code, 200)

    def test_get_specific_order_not_found(self):
        response = requests.get(BASE_URL + "/b3c6a8f4-bdb3-11e8-9747")
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.orders = []