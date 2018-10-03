"""Menu Tests for menu API endpoints."""
from tests.base_test import BaseTest
import json
from . import MENU_DATA

class MenuTest(BaseTest):

    def test_add_menu_without_token(self):
        """Test add menu without token."""
        response = self.app.post(self.base_url + 'admins/menus', json=MENU_DATA)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"

    def test_get_menus_without_token(self):
        """Test for get menus without token."""
        response = self.app.get(self.base_url + 'admins/menus')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"

    def test_get_single_menu_without_token(self):
        """Test for get single menu without token."""
        response = self.app.get(self.base_url + 'admins/menus/1')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"
