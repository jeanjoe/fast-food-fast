from flask import request
from datetime import datetime

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
            "id": self.last_order_id(),
            "menu_id": menu_id,
            "client_id": client_id,
            "location": location,
            "quantity": quantity,
            "status": "pending",
            "created_at": str(datetime.now())
        }
        self.orders.append(order)
        return order

    def last_order_id(self):
        if len(self.orders) < 1:
            return 1
        else:
            return self.orders[-1]['id'] + 1

    def update_order_status(self, order_id, status):
        """Search order and update status if found."""
        order = self.search_order(order_id)        
        if order:
            order[0].update({'status': status})
            return order
        return None

    def update_order_details(self, order_id, location, quantity):
        """Search order and update details if found."""
        order = self.search_order(order_id)        
        if order:
            order[0].update({'location': location, 'quantity': quantity})
            return order
        return None

    def search_order(self, order_id):
        """Search specific order."""
        return [order for order in self.orders if order['id'] == int(order_id)]

class ManageOrder:
    """Manage orders."""

    def __init__(self):
        self.order = Order()
        self.orders = orders
   
    def validate_input(self, validation_data=list):
        """Search order and update status if found."""
        error_message = []
        for data in validation_data:
            try:
                input = request.get_json()
                input[data]
                #Check for empty input
                if not input[data]:
                    raise Exception(data)
            except:
                error_message.append({'field': data, 'message': data + ' is required'})
        #return errors
        return error_message

    def search_duplicate_order(self, client_id, menu_id):
        """Search dulpicate order."""
        for item in self.orders:
            if item['client_id'] == int(client_id) and item['menu_id'] == int(menu_id) and item['status'] == 'pending':
                return True
        return False
