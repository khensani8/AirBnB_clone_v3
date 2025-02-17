#!/usr/bin/python3
"""Create new Flask app; and register the blueprint app_views to Flask instance app.
"""
from flask import Flask,jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
     '''
    Removes the current SQLAlchemy Session object after each request.
    '''
     storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    '''
    Return errmsg `Not Found`.
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
