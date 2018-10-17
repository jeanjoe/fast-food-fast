"""Handle Server error."""
from flask import jsonify
from app import app


@app.errorhandler(400)
def bad_reguset(e):
    """Return Bad Request."""
    return jsonify(error="Bad Request"), 400


@app.errorhandler(404)
def page_not_found(e):
    """Return Page not found"""
    return jsonify(error="Page Not Found error."), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Internal server error."""
    return jsonify(error="Internal server error."), 500


@app.errorhandler(405)
def method_not_allowed(e):
    """Return method, not allowed"""
    return jsonify(error="Method not allowed."), 405
