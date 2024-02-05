#!/usr/bin/python3
"""Create new Flask app; and register the blueprint app_views to Flask instance app.
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views)
