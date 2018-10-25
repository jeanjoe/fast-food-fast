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
        self.cursor.execute(query,
                            (menu_id, client_id, location, quantity, "New",
                             str(datetime.now())))
        return "Order Inserted Successfully"

    def get_all_client_orders(self, client_id):
        """get all client's orders."""
        # return self.select_single_column('orders', 'user_id', client_id)
        query = """SELECT MENUS.ID, MENUS.TITLE, MENUS.DESCRIPTION, MENUS.PRICE, ORDERS.CREATED_AT,
        ORDERS.ID, ORDERS.STATUS, ORDERS.LOCATION, ORDERS.QUANTITY
        FROM MENUS INNER JOIN ORDERS ON ORDERS.MENU_ID = MENUS.ID 
        WHERE USER_ID= %s ORDER BY ORDERS.CREATED_AT DESC;"""
        self.dict_cursor.execute(query, (client_id,))
        orders = self.dict_cursor.fetchall()
        return orders

    def get_specific_client_order(self, client_id, order_id):
        """Get a specific order for a client."""
        query = """SELECT MENUS.ID, MENUS.TITLE, MENUS.DESCRIPTION, MENUS.PRICE, ORDERS.CREATED_AT,
        ORDERS.ID, ORDERS.STATUS, ORDERS.LOCATION, ORDERS.QUANTITY
        FROM MENUS INNER JOIN ORDERS ON ORDERS.MENU_ID = MENUS.ID 
        WHERE ORDERS.ID= %s AND ORDERS.USER_ID= %s ORDER BY ORDERS.CREATED_AT DESC;"""
        self.dict_cursor.execute(query, (order_id, client_id))
        orders = self.dict_cursor.fetchall()
        return orders

    def admin_check_order(self, order_id):
        """Check an order for admin."""
        return self.select_single_column('orders', 'id', order_id)

    def admin_update_menu(self, title, description, price, menu_id):
        """Admin updates specific menu details."""
        query = """
        UPDATE MENUS SET title= %s, description= %s, price= %s WHERE id= %s
        """
        self.cursor.execute(query,
                            (title, description, price, menu_id))
        return True
