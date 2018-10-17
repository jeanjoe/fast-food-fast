"""Define other routs."""
from flask import jsonify
from app import app


@app.route('/', methods=['GET'])
def index():
    """API start route."""
    return jsonify({
        'message':
        'Fast-food-fast API endpoints. Navigate to api/v1/orders'
    }), 200
    