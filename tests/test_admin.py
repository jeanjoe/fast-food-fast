"""Menu Tests for menu API endpoints."""
import json
from tests.base_test import BaseTest
from . import (ADMIN_LOGIN, WRONG_USER_LOGIN, REGISTER_ADMIN,
               REGISTER_USER_RANDOM_EMAIL, MENU_DATA)


class AdminTest(BaseTest):
    """Test Admin endpoints."""

    def test_user_register(self):
        """Test successful admin register."""
        response = self.app.post(
            self.base_url + 'admins/register', json=REGISTER_USER_RANDOM_EMAIL)
        self.assertEqual(response.status_code, 201)
        assert json.loads(
            response.data)['message'] == "Admin registered successfully"

    def test_invalid_register_inputs(self):
        """Test admin register without data"""
        response = self.app.post(self.base_url + 'admins/register')
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['message'] == "Validation error"

    def test_admin_register_email_exist(self):
        """Test admin email exists"""
        self.app.post(self.base_url + 'admins/register', json=REGISTER_ADMIN)
        response = self.app.post(
            self.base_url + 'admins/register', json=REGISTER_ADMIN)
        self.assertEqual(response.status_code, 400)
        assert json.loads(
            response.
            data)['message'] == "This email address is already registered"
        assert json.loads(response.data)['field'] == "email"

    def test_admin_login(self):
        """Test for successful login."""
        self.app.post(self.base_url + 'admins/register', json=REGISTER_ADMIN)
        response = self.app.post(
            self.base_url + 'admins/login', json=ADMIN_LOGIN)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "Login successfully"

    def test_invalid_login_inputs(self):
        """Test validation error."""
        response = self.app.post(self.base_url + 'admins/login')
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['message'] == "Validation error"

    def test_failed_admin_login(self):
        """Test admin failed login."""
        response = self.app.post(
            self.base_url + 'admins/login', json=WRONG_USER_LOGIN)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error'] == "Wrong Email or password"

    def test_admin_update_order_status_without_token(self):
        """Test for update order status without token."""
        response = self.app.put(self.base_url + 'admins/orders/1/update')
        self.assertEqual(response.status_code, 401)
        assert json.loads(
            response.data)['msg'] == "Missing Authorization Header"

    def test_admin_delete_menu(self):
        """Test admin delete menu item."""
        token = self.return_admin_token()
        self.app.post(
            self.base_url + 'admins/menus',
            headers={"Authorization": "Bearer " + token},
            json=MENU_DATA)
        response = self.app.delete(self.base_url + 'admins/menus/1',
            headers={"Authorization": "Bearer " + token})
        self.assertEqual(response.status_code, 200)
        assert json.loads(
            response.data)['message'] == "Menu item deleted successfully"
