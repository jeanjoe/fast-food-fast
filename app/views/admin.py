from app import app
from app.models.admin import Admin
from app.models.menu import MenuModel
from app.models.order import OrderModel
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app.manage import Order, ManageOrder

admin = Admin()
menu = MenuModel()
manage_orders = ManageOrder()
order_model = OrderModel()

@app.route('/api/v1/admin/register', methods=['POST'])
def register_admin():
    validation = manage_orders.validate_input(
        ['first_name', 'last_name', 'email', 'password', 'confirm_password'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 200
    
    #If Validation passes, add to database
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
        return jsonify(admin_token=create_access_token([admin_login, { "account_type": "admin" }]), message="Login successful"), 200
    return jsonify(error="Wrong Email or password"), 401

@app.route('/api/v1/admins/menus', methods=['POST'])
@jwt_required
def admin_add_menu():
    current_user = get_jwt_identity()
    user_type = current_user[1]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    validation = manage_orders.validate_input(['title', 'description', 'price'])
    if validation:
        return jsonify({"message": 'Validation error', "errors": validation}), 400
    get_input = request.get_json()
    save_menu = menu.add_menu(
        current_user[0], get_input['title'], get_input['description'], get_input['price']
    )
    if save_menu:
        return jsonify(menu=save_menu, message="Menu added successfuly", user=current_user)
    return jsonify(error="Unable to record order")

@app.route('/api/v1/admins/menus', methods=['GET'])
@jwt_required
def admin_get_menus():
    current_user = get_jwt_identity()
    user_type = current_user[1]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    menus = menu.get_all_menus()
    return jsonify({"message": "success", "menus": menus}), 200

@app.route('/api/v1/admins/menus<int:menu_id>', methods=['GET'])
@jwt_required
def admin_get_single_menu(menu_id):
    current_user = get_jwt_identity()
    user_type = current_user[1]['account_type']
    if user_type != "admin":
        return jsonify({"error": "Unauthorised Access for none ADMIN accounts"}), 401
    get_menu = menu.get_all_single_menu(menu_id)
    return jsonify({"message": "success", "menus": get_menu}), 200

# @app.route('/api/v1/orders', methods=['GET'])
# def get_all_orders():
#     """Get all orders"""
#     return jsonify({'orders': order_model.get_specific_client_order()}), 200
