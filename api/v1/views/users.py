#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from flask import abort, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from flasgger.utils import swag_from
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/register', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/register_user.yml')
def register_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Name is required")
    if 'email' not in request.get_json():
        abort(400, description="Email is required")
    if 'password' not in request.get_json():
        abort(400, description="Password is required")

    data = request.get_json()
    instance = User(**data)
    try:  # To handle Duplicate email
        # Add the new user to the session
        storage.new(instance)

        # Commit the session to the database
        storage.save()
        # return make_response(jsonify(instance.to_dict()), 201)
        return make_response(jsonify(message="Ok"), 201)
    except IntegrityError:
        return make_response(jsonify(message="Email already exists"), 409)

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User).values()

    if not all_users:
        return make_response(jsonify(message="No users found"), 404)

    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml')
def get_user(user_id):
    """ Retrieves a user by its ID """
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify(message="No user found"), 404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml')
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        return make_response(jsonify(message="No user found"), 404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml')
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        return make_response(jsonify(message="No user found"), 404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(message="User updated"), 200)
