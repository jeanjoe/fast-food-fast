
class Order:

    
    def __init__(self, menu_items = [], orders = []):
        self.menu_items = menu_items
        self.orders = orders

    def get_all_orders(self):
        return self.orders