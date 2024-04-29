#!/usr/bin/python3
"""index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def api_status():
    """
    Retrieve the number of each object type
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Returns the count of each object type.
    """
    object_types = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    counts = {}

    for obj_type in object_types:
        counts[obj_type] = storage.count(obj_type)

    return jsonify(counts)
