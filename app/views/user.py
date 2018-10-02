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

@app.route('/protected')
@jwt_required
def protected():
    # current_user = get_jwt_identity()
    return jsonify(user= get_jwt_identity()[1]['account_type'])

@app.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """Login User."""
    validation = manage_orders.validate_input(['email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    user_login = user.signin_user(get_input['email'], get_input['password'])
    if user_login:
        return jsonify(user_token=create_access_token([user_login, { "account_type": "user" }]), message="Login successfully"), 200
    return jsonify(error="Wrong Email or password"), 401

@app.route('/api/v1/users/orders', methods=['POST'])
@jwt_required
def user_add_order():
    """Add new order to order lists."""
    current_user = get_jwt_identity()
    user_type = current_user[1]['account_type']
    if user_type != "user":
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
        get_input['menu_id'], current_user[0], get_input['location'], get_input['quantity'])
    if not saved_order:
        return jsonify({"error": "Unable process your order"}), 200
    return jsonify({"data": saved_order}), 201

@app.route('/api/v1/users/orders/<int:order_id>')
@jwt_required
def get_user_orders(order_id):
    current_user = get_jwt_identity()
    user_type = current_user[1]['account_type']
    if user_type != "user":
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401
    """get specific order."""
    search_result = order_model.get_specific_client_order(order_id, current_user[0])
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404
    return jsonify({"order": search_result}), 200

# @app.route('/api/v1/users/orders/<int:order_id>', methods=['PUT'])
# @jwt_required
# def update_order_status(order_id):
#     """update order status."""
#     current_user = get_jwt_identity()
#     search_result = order_model.get_specific_client_order(order_id, current_user[0])
#     if not search_result:
#         return jsonify({"message": 'Cannot find this order'}), 404
#     get_input = request.get_json()
#     validation = manage_orders.validate_input(['status'])
#     if validation:
#         return jsonify({"error": validation}), 200

#     update_order = orders.update_order_status(order_id, get_input['status'])
#     return jsonify({"message": update_order}), 200

# @app.route('/api/v1/orders/<int:order_id>/update', methods=['PUT'])
# @jwt_required
# def update_order_details(order_id):
#     """update order details."""
#     get_input = request.get_json()
#     validation = manage_orders.validate_input(['location', 'quantity'])
#     if validation:
#         return jsonify({"error": validation}), 200

#     validate_datatype = manage_orders.validate_datatype(int, [get_input['quantity']])
#     if validate_datatype:
#         return jsonify({"data_type_error": validate_datatype })

#     update_details = orders.update_order_details(
#         order_id, get_input['location'], get_input['quantity'])
#     if update_details:
#         return jsonify({"order": update_details})
#     return jsonify({"error": "Unable to find this order"}), 200

# @app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
# def delete_order(order_id):
#     """Delete order from list."""
#     search_result = orders.search_order(order_id)
#     if not search_result:
#         return jsonify({"message": 'Cannot find this order'}), 404

#     remove_order = orders.delete_order(order_id)
#     if remove_order:
#         return jsonify({"message": "Order deleted successfuly"}), 200
#     return jsonify({"error", "Unable to delete this order"}), 200
