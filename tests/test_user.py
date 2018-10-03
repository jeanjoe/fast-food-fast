"""User Tests for users API endpoints."""
from tests.base_test import BaseTest
import json
from . import MENU_DATA
from . import (REGISTER_USER, USER_LOGIN, WRONG_USER_LOGIN, REGISTER_USER_RANDOM_EMAIL, REGISTER_EMAIL_EXISTS)

class UserTest(BaseTest):

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

    def test_login(self):
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

    def test_get_user_orders_missing_token(self):
        """Test user get orders without token."""
        response = self.app.get(self.base_url + 'users/orders')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header" 
    
    def test_get_user_specifc_order_missing_token(self):
        """Test user get order without token."""
        response = self.app.get(self.base_url + 'users/orders/1')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"
