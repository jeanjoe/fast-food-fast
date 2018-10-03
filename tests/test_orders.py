"""Order Tests for order API endpoints."""
from tests.base_test import BaseTest
import json

class OrderTest(BaseTest):
    """Order Tests."""

    def test_post_order_invalid_token(self):
        """Test for post order without token."""
        response = self.app.post(self.base_url+"users/orders")
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"
