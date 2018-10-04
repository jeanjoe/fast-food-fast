from app import app
from app.models.user import User
from app.models.menu import MenuModel
from app.models.order import OrderModel
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app.manage import Order, ManageOrder
from validate_email import validate_email

user = User()
menu = MenuModel()
manage_orders = ManageOrder()
order_model = OrderModel()

@app.route('/api/v1/admins/register', methods=['POST'])
def register_admin():
    validation = manage_orders.validate_input(
        ['first_name', 'last_name', 'email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    
    #If Validation passes, add to list
    get_input = request.get_json()
    if not validate_email(get_input['email']):
        return jsonify({"error": "Invalid email address"}), 200

    search_duplicate_email = user.search_user('email', get_input['email'].strip())
    if search_duplicate_email:
        return jsonify(field="email", message="This email address is already registered"), 400
    user.register_user(
        get_input['first_name'].strip(), 
        get_input['last_name'].strip(), 
        get_input['email'].strip(), 
        get_input['password'], "admin"
    )
    return jsonify({"message": "User added successfuly"}), 201

@app.route('/api/v1/admins/login', methods=['POST'])
def login_admin():
    """Login Admin."""
    validation = manage_orders.validate_input(['email', 'password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    user_login = user.signin_admin(get_input['email'], get_input['password'])
    if user_login:
        return jsonify(admin_token=create_access_token([user_login]), message="Login successfully"), 200
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
    menu.add_menu(
        current_user[0]['id'], get_input['title'], get_input['description'], get_input['price']
    )
    return jsonify(message="Menu added successfuly"), 201
    
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
        return jsonify({"error": validation}), 400

    if get_input['status'].strip() not in ['COMPLETED', 'ACCEPTED', 'PROCESSING']:
        return jsonify({"error": "Status must be COMPLETED, ACCEPTED OR PROCESSING"}), 200

    update_order = user.admin_update_order(current_user[0]['id'], order_id, get_input['status'].strip())
    if update_order is True:
        return jsonify({"message": "Order status updated successfuly"}), 200