from flask import Flask, jsonify, request
from models.orders import Order, ManageOrder

app = Flask(__name__)
orders = Order()
manage_orders = ManageOrder()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Fast-food-fast API endpoints. Navigate to api/v1/orders'}), 200

@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders.get_all_orders()}), 200

@app.route('/api/v1/orders', methods=['POST'])
def add_order():
    """Add new order to order lists."""
    validation = manage_orders.validate_input(['menu_id', 'client_id', 'location', 'quantity'])
    if validation:
        return jsonify({"error": 'Validation error', "data": validation})

    """If Validation passes, add to list."""
    data = request.get_json()
    saved_order = orders.add_order(data['menu_id'], data['client_id'], data['location'], data['quantity'])
    if not saved_order:
        return jsonify({"error": "Unable process your order"}), 200
    return jsonify({"data": saved_order}), 201

@app.route('/api/v1/orders/<order_id>')
def get_order(order_id):
    search_result = orders.search_order(order_id)
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404
    return jsonify({ "order": search_result}), 200
