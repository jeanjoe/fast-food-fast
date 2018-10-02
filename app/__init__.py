from flask import Flask

app = Flask("__name__")

from app.views import main
from app.views import user
from app.views import admin
from app.models import connection