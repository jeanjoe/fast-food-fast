from flask import Flask, jsonify, request
from models.orders import Order

app = Flask(__name__)
orders = Order()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Fast-food-fast API endpoints. Navigate to api/v1/orders'}), 200

@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders.get_all_orders()}), 200

@app.route('/api/v1/orders', methods=['POST'])
def add_order():
    """Add new order to order lists."""
    data = request.get_json()
    saved_order = orders.add_order(data['menu_id'], data['client_id'], data['location'], data['quantity'])
    if not saved_order:
        return jsonify({"error": "Unable process your order"})
    return jsonify({"data": saved_order}), 201
