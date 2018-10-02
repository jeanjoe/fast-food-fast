"""Orders API endpoints."""
from app import app
from flask import jsonify
from app.models.migration import Migration
from flask_jwt_extended import (JWTManager)

app.config.from_object('config')
app.config['SECRET_KEY']
jwt = JWTManager(app)
db = Migration()
db.create_tables()