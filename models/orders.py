from flask import request
from datetime import datetime
import uuid

menu_items = []
orders = []

class Order:

    def __init__(self):
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

    def update_order_status(self, order_id, status):
        """Search order and update status if found."""
        order = self.search_order(order_id)        
        if order:
            order[0].update({'status': status})
            return order
        return None

    def search_order(self, order_id):
        return [order for order in self.orders if order['id'] == order_id]

class ManageOrder:

    def __init__(self):
        self.order = Order()
        self.orders = orders
   
    def validate_input(self, validation_data = []):
        error_message = []
        for data in validation_data:
            try:
                input = request.get_json()
                input[data]
                """Check for empty input."""
                if not input[data]:
                    raise Exception(data)
            except Exception as ex:
                error_message.append({ 'field' : str(ex), 'message': str(ex) + ' is required' })
        #return errors
        return error_message

    def search_duplicate_order(self, client_id, menu_id):
        result = False 
        for item in self.orders:
            if item['client_id'] == client_id and item['menu_id'] == menu_id and item['status'] == 'pending':
                result = True
        return result