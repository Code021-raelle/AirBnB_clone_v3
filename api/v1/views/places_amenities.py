#!/usr/bin/python3
"""Script that link between Place objects and Amenity objects
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views

places_amenities = Blueprint('places_amenities', __name__)


@places_amenities.route('/places/<place_id>/amenities', methods=['GET'],
        strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@places_amenities.route('/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@places_amenities.route('/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
