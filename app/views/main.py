"""Orders API endpoints."""
from app import app
from flask import jsonify
from flask_jwt_extended import (JWTManager)

app.config.from_object('config')
app.config['SECRET_KEY']
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    """API start route."""
    return jsonify({'message': 'Fast-food-fast API endpoints. Navigate to api/v1/orders'}), 200