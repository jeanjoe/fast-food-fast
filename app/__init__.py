from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

app = Flask("__name__")
CORS(app)

swagger = Swagger(app)

from app.views import main
from app.views import user
from app.views import admin
from app.views import errors
from app.models import connection
