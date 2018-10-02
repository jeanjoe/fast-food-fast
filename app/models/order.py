from app.models.connection import DatabaseConnection
from datetime import datetime

class OrderModel(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def add_order(self,menu_id, client_id, location, quantity):
        """Create new Order."""
        try:
            query= """
            INSERT INTO ORDERS (menu_id, user_id, location, quantity, status, created_at) VALUES
            ({}, '{}', '{}', {}, 'New', '{}')
            """.format(menu_id, client_id, location, quantity, str(datetime.now()))
            self.cursor.execute(query)
            return "Data Inserted Successfully"
        except Exception as error:
            return "Unable to save error {} ".format(str(error))

    def get_all_client_orders(self, client_id):
        """get all client's orders."""
        try:
            query= """SELECT * FROM ORDERS WHERE USER_ID= %s """
            self.dict_cursor.execute(query, (client_id,))
            orders = self.dict_cursor.fetchall()
            return orders
        except Exception as error:
            print(str(error))
            return str(error)

    def get_specific_client_order(self, client_id, order_id):
        """Get a specific order for a client."""
        query= """SELECT * FROM ORDERS WHERE ID= %s AND USER_ID= %s"""
        self.dict_cursor.execute(query, (order_id, client_id))
        orders = self.dict_cursor.fetchall()
        return orders

    def admin_check_order(self, order_id):
        """Check an order for admin."""
        query= """SELECT * FROM ORDERS WHERE ID= %s"""
        self.dict_cursor.execute(query, (order_id,))
        order = self.dict_cursor.fetchone()
        return order