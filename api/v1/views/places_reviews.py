#!/usr/bin/python3
"""Script for Review objects that handles all default RESTful API
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(city_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user_id = data['user_id']
    if storage.get("User", user_id) is None:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    for key, value in data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    return jsonify({}), 200
