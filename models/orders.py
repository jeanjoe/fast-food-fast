from flask import request
from datetime import datetime
import uuid

class Order:

    
    def __init__(self, menu_items = [], orders = []):
        self.menu_items = menu_items
        self.orders = orders

    def get_all_orders(self):
        """Get list of all orders."""
        return self.orders

    def add_order(self, menu_id, client_id, location, quantity):
        """Create New order."""
        order = {
            "id": str(uuid.uuid1()),
            "menu_id": menu_id,
            "client_id": client_id,
            "location": location,
            "quantity": quantity,
            "status": "pending",
            "created_at": str(datetime.now())
        }
        self.orders.append(order)
        return order

    def search_order(self, order_id):
        return [order for order in self.orders if order['id'] == order_id]

class ManageOrder:
   
    def validate_input(self, validation_data = []):
        error_message = []
        for data in validation_data:
            try:
                input = request.get_json()
                input[data]
            except Exception as ex:
                error_message.append({ 'field' : str(ex), 'message': str(ex) + ' is required' })
        #return errors
        return error_message
