"""Tests for API endpoints."""
import unittest
import json
from app import app
from app.models.migration import Migration
from . import *

BASE_URL = "/api/v1/"
migration = Migration()

class BaseTest(unittest.TestCase):
    """Setting up testing data for Tests."""

    def setUp(self):
        self.base_url = BASE_URL
        self.app = app.test_client()
        migration.create_tables()

    def tearDown(self):
        self.migration = migration.truncate_tables(['orders', 'menus', 'users'])

    def return_admin_token(self):
        self.app.post(self.base_url + "admins/register", json=REGISTER_ADMIN)
        response = self.app.post(self.base_url + "admins/login", json=ADMIN_LOGIN)
        return json.loads(response.data)['admin_token']

    def return_user_token(self):
        """Return user token."""
        self.app.post(self.base_url + 'users/register', json=REGISTER_USER)
        response = self.app.post(self.base_url + 'users/login', json=USER_LOGIN)
        return json.loads(response.data)['user_token']
