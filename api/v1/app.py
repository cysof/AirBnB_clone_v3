#!/usr/bin/python3
"""Contains a Flask web application API."""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

# Create a Flask application instance
app = Flask(__name__)

# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)


# Declare a method to handle @app.teardown_app context
# that calls storage.close function
@app.teardown_appcontext
def teardown_flask(exception):
    """Closes the storage"""
    storage.close()


# Error handlers
@app.errorhandler(404)
def error_404(error):
    """Handles 404 HTTP error"""
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """Handles the 400 HTTP error code"""
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


# Run Flask Server
if __name__ == "__main__":
    # Define host and port based on environment variables
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # Run Flask application
    app.run(host=host, port=port, threaded=True)
