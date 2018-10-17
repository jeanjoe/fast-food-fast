"""Define other routs."""
from flask import jsonify, render_template
from app import app


@app.route('/', methods=['GET'])
def index():
    """API start route."""
    # return jsonify({
    #     'message':
    #     'Fast-food-fast API endpoints. Navigate to api/v1/orders'
    # }), 200

    return render_template('index.html')

@app.route('/user/login', methods=['GET'])
def user_login():
    """Render user login page"""
    return render_template('sign-in.html')

@app.route('/user/register', methods=['GET'])
def user_registration():
    """Render user register page."""
    return render_template('sign-up.html')

@app.route('/admin/login', methods=['GET'])
def admin_login():
    """Render admin login page"""
    return render_template('admin/sign-in.html')

@app.route('/admin/register', methods=['GET'])
def admin_registration():
    """Render admin register page."""
    return render_template('admin/sign-up.html')