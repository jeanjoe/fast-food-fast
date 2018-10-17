"""Initialize modules"""
from flask_jwt_extended import (JWTManager)
from flask import jsonify
from app.models.migration import Migration
from app import app

app.config.from_object('config')
app.config['SECRET_KEY']
JWT = JWTManager(app)
DB = Migration()
DB.create_tables()
