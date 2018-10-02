from app import app
from app.models.user import User
from app.models.menu import MenuModel
from app.models.order import OrderModel
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app.manage import Order, ManageOrder

user = User()
menu = MenuModel()
manage_orders = ManageOrder()
order_model = OrderModel()

@app.route('/api/v1/admin/register', methods=['POST'])
def register_admin():
    validation = manage_orders.validate_input(
        ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 200
    
    #If Validation passes, add to list
    get_input = request.get_json()
    search_duplicate_email = user.search_user('email', get_input['email'])
    if search_duplicate_email:
        return jsonify(field="email", message="This email address is already registered"), 400
    save_user = user.register_user(
        get_input['first_name'], get_input['last_name'], get_input['email'], get_input['phone'],
        get_input['password'], "admin"
    )
    if save_user is True:
        return jsonify({"message": "User added successfuly"}), 201
    return jsonify({"error": "Unable to register this user", "reason": save_user}), 200

@app.route('/api/v1/admin/login', methods=['POST'])
def login_admin():
    """Login Admin."""
    validation = manage_orders.validate_input(['email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    user_login = user.signin_admin(get_input['email'], get_input['password'])
    if user_login:
        return jsonify(user_token=create_access_token([user_login]), message="Login successfully"), 200
    return jsonify(error="Wrong Email or password"), 400

@app.route('/api/v1/admins/menus', methods=['POST'])
@jwt_required
def admin_add_menu():
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    validation = manage_orders.validate_input(['title', 'description', 'price'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    save_menu = menu.add_menu(
        current_user[0]['id'], get_input['title'], get_input['description'], get_input['price']
    )
    if save_menu:
        return jsonify(menu=save_menu, message="Menu added successfuly")
    return jsonify(error="Unable to record order")

@app.route('/api/v1/admins/menus', methods=['GET'])
@jwt_required
def admin_get_menus():
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    menus = menu.get_all_menus()
    return jsonify({"message": "success", "menus": menus}), 200

@app.route('/api/v1/admins/menus/<int:menu_id>', methods=['GET'])
@jwt_required
def admin_get_single_menu(menu_id):
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    get_menu = menu.get_all_single_menu(menu_id)
    return jsonify({"message": "success", "menus": get_menu}), 200

@app.route('/api/v1/admins/orders', methods=['GET'])
@jwt_required
def get_all_orders():
    """Get all orders"""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    return jsonify({'orders': user.admin_get_orders()}), 200

@app.route('/api/v1/admins/orders/<int:order_id>/update', methods=['PUT'])
@jwt_required
def update_specific_order_status(order_id):
    """update order status."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401

    search_result = order_model.admin_check_order(order_id)
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404

    get_input = request.get_json()
    validation = manage_orders.validate_input(['status'])
    if validation:
        return jsonify({"error": validation}), 200

    update_order = user.admin_update_order(current_user[0]['id'], order_id, get_input['status'])
    if update_order is True:
        return jsonify({"message": "order updated successfuly"}), 200