"""Model for supporting DB operations."""
from datetime import datetime
from .connection import DatabaseConnection

class OrderModel(DatabaseConnection):
    """Order Model."""

    def add_order(self, menu_id, client_id, location, quantity):
        """Create new Order."""
        query = """
        INSERT INTO ORDERS (menu_id, user_id, location, quantity, status, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.cursor.execute(
            query, (menu_id, client_id, location, quantity, "New", str(datetime.now()))
        )
        return "Order Inserted Successfully"

    def get_all_client_orders(self, client_id):
        """get all client's orders."""
        return self.select_single_column('orders', 'user_id', client_id)

    def get_specific_client_order(self, client_id, order_id):
        """Get a specific order for a client."""
        query = """SELECT * FROM ORDERS WHERE ID= %s AND USER_ID= %s;"""
        self.dict_cursor.execute(query, (order_id, client_id))
        orders = self.dict_cursor.fetchall()
        return orders

    def admin_check_order(self, order_id):
        """Check an order for admin."""
        return self.select_single_column('orders', 'id', order_id)
