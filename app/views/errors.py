from app import app
from flask import jsonify

@app.errorhandler(400)
def bad_reguset(e):
    return jsonify(error="Bad Request"), 400

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Page Not Found error."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error."), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error="Method not allowed."), 405
