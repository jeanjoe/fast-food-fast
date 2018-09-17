from flask import Flask, jsonify
from modules.orders import Order


app = Flask(__name__)
orders = Order()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Fast-food-fast API endpoints. Navigate to api/v1/orders'}), 200

@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders.get_all_orders()}), 200

if __name__ == '__main__':
    app.run(debug=True)