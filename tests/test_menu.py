from app import app
import json
import unittest
from . import MENU_DATA

BASE_URL = "/api/v1/"

class MenuTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_add_menu(self):
        response = self.app.post(BASE_URL + 'admins/menus', json=MENU_DATA)
        # self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "Menu added successfuly"

    def test_add_menu_without_token(self):
        response = self.app.post(BASE_URL + 'admins/menus', json=MENU_DATA)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"

    def test_get_menus(self):
        response = self.app.get(BASE_URL + 'admins/menus')
        self.assertEqual(response.status_code, 200)

    def test_get_single_menu(self):
        response = self.app.post(BASE_URL + 'admins/menus/1')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        pass