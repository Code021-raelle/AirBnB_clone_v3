#!/usr/bin/python3
""" api/v1/app.py
"""
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.views.places_amenities import places_amenities
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(places_amenities)


cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(error):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
