"""Tests for API endpoints."""
import unittest
import random
import json
from app import app
from app.models.connection import DatabaseConnection
from app.models.migration import Migration

BASE_URL = "/api/v1/"
migration = Migration()

class BaseTest(unittest.TestCase, DatabaseConnection):
    """Setting up testing data for Tests."""

    def setUp(self):
        self.base_url = BASE_URL
        self.app = app.test_client()

    def tearDown(self):
        self.migration = migration.truncate_tables(['orders', 'menus', 'users'])
