from app import app
from flask import jsonify

@app.route('/', methods=['GET'])
def index():
    """API start route."""
    return jsonify({'message': 'Fast-food-fast API endpoints. Navigate to api/v1/orders'}), 200