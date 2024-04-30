#!/usr/bin/python3
"""Script to implement the view for User
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(Users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'email' not in request.json:
        abort(400, description="Missing email")
    if 'password' not in request.json:
        abort(400, description="Missing password")
    data = request.json
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({}), 200
