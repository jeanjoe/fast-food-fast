"""User Tests for users API endpoints."""
from tests.base_test import BaseTest
import json
from . import MENU_DATA
from . import (REGISTER_USER, USER_LOGIN, WRONG_USER_LOGIN, REGISTER_USER_RANDOM_EMAIL, 
REGISTER_EMAIL_EXISTS, ORDER_DATA)

class UserTest(BaseTest):

    def test_main_end_point(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_user_register(self):
        """Test successful register"""
        response = self.app.post(self.base_url + 'users/register', json=REGISTER_USER_RANDOM_EMAIL)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['message'] == "User added successfuly"

    def test_invalid_register_inputs(self):
        """Test register without data"""
        response = self.app.post(self.base_url + 'users/register')
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['message'] == "Validation error"

    def test_user_register_email_exist(self):
        """Test user email exists."""
        self.app.post(self.base_url + 'users/register', json=REGISTER_USER)
        response = self.app.post(self.base_url + 'users/register', json=REGISTER_USER)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "This email address is already registered"

    def test_successful_user_login(self):
        """Test successful login."""
        self.app.post(self.base_url + 'users/register', json=REGISTER_USER)
        response = self.app.post(self.base_url + 'users/login', json=USER_LOGIN)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "Login successfully"

    def test_invalid_login_inputs(self):
        """Test missing login email and password."""
        response = self.app.post(self.base_url + 'users/login')
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['message'] == "Validation error"

    def test_failed_user_login(self):
        """Test user login with wrong credentials."""
        response = self.app.post(self.base_url + 'users/login', json=WRONG_USER_LOGIN)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['error'] == "Wrong Email or password"

    def test_user_get_orders_with_admin_token(self):
        token = self.return_admin_token()
        response = self.app.get(self.base_url + "users/orders", 
        headers=dict(Authorization= "Bearer " + token))
        assert response.status_code == 401
        self.assertEqual(json.loads(response.data)['error'], "Unauthorised Access for none user accounts")

    def test_user_get_orders_with_user_token(self):
        token = self.return_user_token()
        response = self.app.get(self.base_url + "users/orders", headers=dict(Authorization= "Bearer " + token))
        assert response.status_code == 200
        self.assertIsInstance(json.loads(response.data)['order'], list)

    def test_user_post_orders_with_admin_token(self):
        token = self.return_admin_token()
        response = self.app.post(self.base_url + "users/orders", 
        headers=dict(Authorization= "Bearer " + token))
        assert response.status_code == 401
        self.assertEqual(json.loads(response.data)['error'], "Unauthorised Access for none user accounts")

    def test_user_post_orders_with_user_token_without_data(self):
        token = self.return_user_token()
        response = self.app.post(self.base_url + "users/orders", headers=dict(Authorization= "Bearer " + token))
        assert response.status_code == 400
        self.assertEqual(json.loads(response.data)['message'], "Validation error")

    def test_user_post_orders_with_user_token_wrong_menu(self):
        token = self.return_user_token()
        response = self.app.post(
            self.base_url + "users/orders", 
            headers=dict(Authorization= "Bearer " + token),
            json=ORDER_DATA
        )
        assert response.status_code == 404
        assert json.loads(response.data)['error'] == "This menu item doesn't exist in the menu list"

    def test_user_post_orders_with_user_token_with_menu_exists(self):
        admin_token = self.return_admin_token()
        self.app.post(
            self.base_url + 'admins/menus', 
            headers={"Authorization": "Bearer " + admin_token}, 
            json=MENU_DATA
        )
        token = self.return_user_token()
        response = self.app.post(
            self.base_url + "users/orders", 
            headers=dict(Authorization= "Bearer " + token),
            json=ORDER_DATA
        )
        assert response.status_code == 201
        assert json.loads(response.data)['data'] == "Order Inserted Successfully"

    def test_get_user_orders_missing_token(self):
        """Test user get orders without token."""
        response = self.app.get(self.base_url + 'users/orders')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header" 
    
    def test_get_user_specific_order_without_token(self):
        """Test user get order without token."""
        response = self.app.get(self.base_url + 'users/orders/1')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"

    def test_get_user_specific_order_with_admin_token(self):
        token = self.return_admin_token()
        response = self.app.get(
            self.base_url + 'users/orders/1', 
            headers={"Authorization": "Bearer " + token}
        )
        assert response.status_code == 401
        self.assertEqual(json.loads(response.data)['error'], "Unauthorised Access for none user accounts")

    def test_get_user_specific_order_not_found_with_user_token(self):
        token = self.return_user_token()
        response = self.app.get(
            self.base_url + 'users/orders/1', 
            headers={"Authorization": "Bearer " + token}
        )
        assert response.status_code == 404
        self.assertEqual(json.loads(response.data)['message'], "Cannot find this order")

    def test_get_user_specific_order_with_user_token(self):
        token = self.return_user_token()
        response = self.app.get(
            self.base_url + 'users/orders/1', 
            headers={"Authorization": "Bearer " + token}
        )
        assert response.status_code == 404
        self.assertEqual(json.loads(response.data)['message'], "Cannot find this order")
    def test_user_get_specific_order(self):
        token = self.return_user_token()
        admin_token = self.return_admin_token()
        self.app.post(
            self.base_url + 'admins/menus', 
            headers={"Authorization": "Bearer " + admin_token}, 
            json=MENU_DATA
        )
        self.app.post(
            self.base_url + "users/orders", 
            json=ORDER_DATA,
            headers={"Authorization": "Bearer " + token }
        )
        response = self.app.get(
            self.base_url + "users/orders/1",
            headers={"Authorization": "Bearer " + token }
        )
        assert response.status_code == 200
        self.assertIsInstance(json.loads(response.data)['order'], list)