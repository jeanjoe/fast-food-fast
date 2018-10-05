"""Menu Tests for menu API endpoints."""
import json
from tests.base_test import BaseTest
from . import MENU_DATA

class MenuTest(BaseTest):
    """Testb menu endpoints."""

    def test_add_menu_without_token(self):
        """Test add menu without token."""
        response = self.app.post(self.base_url + 'admins/menus', json=MENU_DATA)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"

    def test_add_menu_with_token(self):
        """Test add menu without token."""
        admin_token = self.return_admin_token()
        response = self.app.post(
            self.base_url + 'admins/menus',
            headers={"Authorization": "Bearer " + admin_token},
            json=MENU_DATA
        )
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['message'] == "Menu added successfully"

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

    def test_admin_get_all_menus(self):
        """Test admn get all menus."""
        token = self.return_admin_token()
        response = self.app.get(
            self.base_url + "admins/menus",
            headers={"Authorization": "Bearer " + token}
        )
        assert response.status_code == 200
        self.assertIsInstance(json.loads(response.data)['menus'], list)

    def test_admin_get_all_orders(self):
        """Test admin Get all orders."""
        token = self.return_admin_token()
        response = self.app.get(
            self.base_url + "admins/orders",
            headers={"Authorization": "Bearer " + token}
        )
        assert response.status_code == 200
        self.assertIsInstance(json.loads(response.data)['orders'], list)
