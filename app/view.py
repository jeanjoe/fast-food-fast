"""Orders API endpoints."""
from app import app
from app.models.user import User
from app.models.admin import Admin
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from .manage import Order, ManageOrder
from app.models.migration import Migration

app.config.from_object('config')
app.config['SECRET_KEY']
jwt = JWTManager(app)

migration = Migration()
migration.create_tables()

user = User()
admin = Admin()
orders = Order()
manage_orders = ManageOrder()

@app.route('/', methods=['GET'])
def index():
    """API start route."""
    return jsonify({'message': 'Fast-food-fast API endpoints. Navigate to api/v1/orders'}), 200

@app.route('/api/v1/users/register', methods=['POST'])
def register_user():
    validation = manage_orders.validate_input(
        ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 200
    
    #If Validation passes, add to list
    get_input = request.get_json()
    search_duplicate_email = user.search_user('email', get_input['email'])
    if search_duplicate_email:
        return jsonify(fiel="email", message="This email address is already registered"), 200
    save_user = user.register_user(
        get_input['first_name'], get_input['last_name'], get_input['email'], get_input['phone'],
        get_input['password']
    )
    if save_user is True:
        return jsonify({"message": "User added successfuly"}), 200
    return jsonify({"error": "Unable to register this user", "reason": save_user}), 200

@app.route('/api/v1/users/login', methods=['POST'])
def login_user():
    validation = manage_orders.validate_input(['email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    user_login = user.signin_user(get_input['email'], get_input['password'])
    if user_login:
        return jsonify(user=create_access_token(user_login)), 200
    return jsonify(error="Wrong Email or password"), 401

@app.route('/api/v1/admin/register', methods=['POST'])
def register_admin():
    validation = manage_orders.validate_input(
        ['first_name', 'last_name', 'email', 'password', 'confirm_password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 200
    
    #If Validation passes, add to list
    get_input = request.get_json()
    search_duplicate_email = admin.search_admin('email', get_input['email'])
    if search_duplicate_email:
        return jsonify(fiel="email", message="This email address is already registered"), 200
    save_admin = admin.register_admin(
        get_input['first_name'], get_input['last_name'], get_input['email'], get_input['password']
    )
    if save_admin is True:
        return jsonify({"message": "User added successfuly"}), 200
    return jsonify({"error": "Unable to register this user", "reason": save_admin}), 200

@app.route('/api/v1/admin/login', methods=['POST'])
def login_admin():
    validation = manage_orders.validate_input(['email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    admin_login = admin.signin_admin(get_input['email'], get_input['password'])
    if admin_login:
        return jsonify(user=create_access_token(admin_login), message="Login successful"), 200
    return jsonify(error="Wrong Email or password"), 401
    
@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    """Get all orders"""
    return jsonify({'orders': orders.get_all_orders()}), 200

@app.route('/api/v1/orders', methods=['POST'])
@jwt_required
def admin_add_order():
    """Add new order to order lists."""
    validation = manage_orders.validate_input(['menu_id', 'location', 'quantity'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    
    #If Validation passes, add to list
    get_input = request.get_json()
    validate_datatype = manage_orders.validate_datatype(
        int, [get_input['menu_id'], get_input['client_id'], get_input['quantity'] ])
    if validate_datatype:
        return jsonify({"data_type_error": validate_datatype }), 200

    #Validate duplicates
    if manage_orders.search_duplicate_order(get_input['client_id'], get_input['menu_id']):
        return jsonify({"error": "This order has already been registered"}), 200
    saved_order = orders.add_order(
        get_input['menu_id'], get_input['client_id'], get_input['location'], get_input['quantity'])
    if not saved_order:
        return jsonify({"error": "Unable process your order"}), 200
    return jsonify({"data": saved_order}), 201

@app.route('/api/v1/orders/<int:order_id>')
def get_order(order_id):
    """get specific order."""
    search_result = orders.search_order(order_id)
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404
    return jsonify({"order": search_result}), 200

@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    """update order status."""
    get_input = request.get_json()
    validation = manage_orders.validate_input(['status'])
    if validation:
        return jsonify({"error": validation}), 200

    update_order = orders.update_order_status(order_id, get_input['status'])
    if update_order:
        return jsonify({"data": update_order}), 200
    return jsonify({"error": "Unable to find this order"}), 404

@app.route('/api/v1/orders/<int:order_id>/update', methods=['PUT'])
def update_order_details(order_id):
    """update order details."""
    get_input = request.get_json()
    validation = manage_orders.validate_input(['location', 'quantity'])
    if validation:
        return jsonify({"error": validation}), 200

    validate_datatype = manage_orders.validate_datatype(int, [get_input['quantity']])
    if validate_datatype:
        return jsonify({"data_type_error": validate_datatype })

    update_details = orders.update_order_details(
        order_id, get_input['location'], get_input['quantity'])
    if update_details:
        return jsonify({"order": update_details})
    return jsonify({"error": "Unable to find this order"}), 200

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete order from list."""
    search_result = orders.search_order(order_id)
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404

    remove_order = orders.delete_order(order_id)
    if remove_order:
        return jsonify({"message": "Order deleted successfuly"}), 200
    return jsonify({"error", "Unable to delete this order"}), 200
