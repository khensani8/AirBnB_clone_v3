#!/usr/bin/python3
"""Create new Flask app; and register the blueprint app_views to Flask instance app.
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
