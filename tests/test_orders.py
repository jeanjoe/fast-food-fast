"""Order Tests for order API endpoints."""
from tests.base_test import BaseTest
import json
from . import *

class OrderTest(BaseTest):
    """Order Tests."""

    def test_post_order_invalid_token(self):
        """Test for post order without token."""
        response = self.app.post(self.base_url+"users/orders")
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"

    def test_admin_update_order_status(self):
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
        response = self.app.put(
            self.base_url + "admins/orders/1/update",
            headers={"Authorization": "Bearer " + admin_token },
            json={ "status": "Completed"})
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == "Order status updated successfuly"
