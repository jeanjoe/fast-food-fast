"""Endpoints for admin."""
from flasgger import swag_from
from validate_email import validate_email
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import jsonify, request
from app import app
from app.models.user import User
from app.models.menu import MenuModel
from app.models.order import OrderModel
from .validator import InputValidator

user = User()
menu = MenuModel()
input_validator = InputValidator()
order_model = OrderModel()


@app.route('/api/v1/admins/register', methods=['POST'])
@swag_from('../docs/admin_signup.yml')
def register_admin():
    """Register new admin."""
    validation = input_validator.validate_input(
        ['first_name', 'last_name', 'email', 'password'])
    if validation:
        return jsonify({
            "message": 'Validation error',
            "errors": validation
        }), 400

    #If Validation passes, add to list
    get_input = request.get_json()
    if not validate_email(get_input['email']):
        return jsonify({"error": "Invalid email address"}), 200

    search_duplicate_email = user.search_user('email',
                                              get_input['email'].strip())
    if search_duplicate_email:
        return jsonify(
            field="email",
            message="This email address is already registered"), 400
    user.register_user(
        get_input['first_name'].strip(), get_input['last_name'].strip(),
        get_input['email'].strip(), get_input['password'], "admin")
    return jsonify({"message": "Admin registered successfully"}), 201


@app.route('/api/v1/admins/login', methods=['POST'])
@swag_from('../docs/admin_signin.yml')
def login_admin():
    """Login Admin."""
    validation = input_validator.validate_input(['email', 'password'])
    if validation:
        return jsonify({
            "message": 'Validation error',
            "errors": validation
        }), 400
    get_input = request.get_json()
    user_login = user.signin_admin(get_input['email'], get_input['password'])
    if user_login:
        return jsonify(
            admin_token=create_access_token([user_login]),
            message="Login successfully"), 200
    return jsonify(error="Wrong Email or password"), 400


@app.route('/api/v1/admins/menus', methods=['POST'])
@jwt_required
@swag_from('../docs/admin_add_menu.yml')
def admin_add_menu():
    """Admin to add new menu item."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    validation = input_validator.validate_input(
        ['title', 'description', 'price'])
    if validation:
        return jsonify({
            "message": 'Validation error',
            "errors": validation
        }), 400
    get_input = request.get_json()
    menu.add_menu(current_user[0]['id'], get_input['title'],
                  get_input['description'], get_input['price'])
    return jsonify(message="Menu added successfully"), 201


@app.route('/api/v1/admins/menus/<int:menu_id>/update', methods=['PUT'])
@jwt_required
@swag_from('../docs/admin_update_menu.yml')
def admin_update_menu_details(menu_id):
    """Admin to add update menu item."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    validation = input_validator.validate_input(
        ['title', 'description', 'price'])
    if validation:
        return jsonify({
            "message": 'Validation error',
            "errors": validation
        }), 400
    get_input = request.get_json()
    order_model.admin_update_menu(get_input['title'], get_input['description'],
                  get_input['price'], menu_id)
    return jsonify(message="Menu Updated successfully"), 200


@app.route('/api/v1/admins/menus/<int:menu_id>', methods=['DELETE'])
@jwt_required
@swag_from('../docs/admin_delete_menu.yml')
def admin_delete_menu_item(menu_id):
    """Admin delete menu item."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401

    get_menu = menu.get_a_single_menu(menu_id)
    status = 200
    response = {"message": "Menu item deleted successfully"}
    if not get_menu:
        response = {"not_found_error": "This menu Item does not exist"}
        status = 404
        # return jsonify(response), status

    menu.admin_delete_menu_item(menu_id)
    return jsonify(response), status
    

@app.route('/api/v1/admins/menus', methods=['GET'])
@jwt_required
@swag_from('../docs/admin_get_menus.yml')
def admin_get_menus():
    """Admin endpoint for getting all menus."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    menus = menu.get_all_menus()
    return jsonify({"message": "success", "menus": menus}), 200


@app.route('/api/v1/admins/menus/<int:menu_id>', methods=['GET'])
@jwt_required
@swag_from('../docs/admin_get_a_menu.yml')
def admin_get_single_menu(menu_id):
    """Admin endpoint for getting a single menu."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    get_menu = menu.get_a_single_menu(menu_id)
    status = 200
    response = {"message": "success", "menus": get_menu}
    if not get_menu:
        response = {"message": "This menu Item does not exist"}
        status = 404
    return jsonify(response), status


@app.route('/api/v1/admins/orders', methods=['GET'])
@jwt_required
@swag_from('../docs/admin_get_orders.yml')
def get_all_orders():
    """Get all new orders"""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    return jsonify({'orders': user.admin_get_orders('new')}), 200


@app.route('/api/v1/admins/orders/history', methods=['GET'])
@jwt_required
@swag_from('../docs/admin_get_order_history.yml')
def get_all_order_history():
    """Get all processed orders"""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    return jsonify({'orders': user.admin_get_orders('history')}), 200


@app.route('/api/v1/admins/orders/<int:order_id>/update', methods=['PUT'])
@jwt_required
@swag_from('../docs/admin_update_order.yml')
def update_specific_order_status(order_id):
    """update order status."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401

    search_result = order_model.admin_check_order(order_id)
    if not search_result:
        return jsonify({"message": 'Cannot find this order'}), 404

    get_input = request.get_json()
    validation = input_validator.validate_input(['status'])
    if validation:
        return jsonify({"error": validation}), 400

    user.admin_update_order(current_user[0]['id'], order_id,
                            get_input['status'].strip())
    return jsonify({"message": "Order status updated successfully"}), 200


@app.route('/api/v1/admins/orders/<int:order_id>')
@jwt_required
@swag_from('../docs/admin_get_an_order.yml')
def admin_get_specific_order(order_id):
    """Admin get specific order."""
    current_user = get_jwt_identity()
    user_type = current_user[0]['account_type']
    if user_type != "admin":
        return jsonify({
            "error": "Unauthorised Access for none ADMIN accounts"
        }), 401
    order = order_model.admin_check_order(order_id)
    
    status = 200
    response = {"message": "success", "order": order}
    if not order:
        response = {"message": "This Order does not exist"}
    return jsonify(response), status
