from app import app
from app.models.user import User
from app.models.order import OrderModel
from app.models.menu import MenuModel
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app.manage import Order, ManageOrder

user = User()
order_model = OrderModel()
menu = MenuModel()
manage_orders = ManageOrder()

@app.route('/api/v1/users/register', methods=['POST'])
def register_user():
    """Register User."""
    validation = manage_orders.validate_input(
        ['first_name', 'last_name', 'email', 'phone', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    
    #If Validation passes, add to list
    get_input = request.get_json()
    search_duplicate_email = user.search_user('email', get_input['email'])
    if search_duplicate_email:
        return jsonify(field="email", message="This email address is already registered"), 200
    user.register_user(
        get_input['first_name'], get_input['last_name'], get_input['email'], get_input['phone'],
        get_input['password'], "client"
    )
    return jsonify({"message": "User added successfuly"}), 201

@app.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """Login User."""
    validation = manage_orders.validate_input(['email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    user_login = user.signin_user(get_input['email'], get_input['password'])
    if user_login:
        return jsonify(user_token=create_access_token([user_login]), message="Login successfully"), 200
    return jsonify(error="Wrong Email or password"), 401

@app.route('/api/v1/users/orders', methods=['POST'])
@jwt_required
def user_add_order():
    """Add new order to order lists."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "client":
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401
    validation = manage_orders.validate_input(['menu_id', 'location', 'quantity'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    
    #If Validation passes, add to list
    get_input = request.get_json()
    validate_datatype = manage_orders.validate_datatype(
        int, [get_input['menu_id'], get_input['quantity'] ])
    if validate_datatype:
        return jsonify({"data_type_error": validate_datatype }), 200

    search_menu = menu.get_all_single_menu(get_input['menu_id'])
    if not search_menu:
        return jsonify(error="This menu item doesn't exist in the menu list"), 404
    
    saved_order = order_model.add_order(
        get_input['menu_id'], current_user[0]['id'], get_input['location'], get_input['quantity'])
    if not saved_order:
        return jsonify({"error": "Unable process your order"}), 200
    return jsonify({"data": saved_order}), 201

@app.route('/api/v1/users/orders/<int:order_id>')
@jwt_required
def get_user_specific_order(order_id):
    """get specific order."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "client":
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401

    search_result = order_model.get_specific_client_order( current_user[0]['id'], order_id)
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404
    return jsonify({"order": search_result}), 200

@app.route('/api/v1/users/orders', methods=['GET'])
@jwt_required
def get_current_user_orders():
    """update order status."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "client":
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401
    search_result = order_model.get_all_client_orders(current_user[0]['id'])
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404
    return jsonify({"order": search_result}), 200
