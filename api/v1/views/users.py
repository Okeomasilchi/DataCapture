#!/usr/bin/python3

"""
Models for the routes of the User_views
"""


from flask import abort, request
from hashlib import md5
from json import dumps as js
from api.v1.views import user_views
from models import storage
from models.user import User
from utils.validators import parse_dict, validate_password
from utils.error import log_error

@user_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    Retrieves all users from storage and returns a list
    of their dictionaries.
    """
    try:
        users = storage.all(User).values()

        if not users:
            return js([])

        return js([user.to_dict() for user in users])
    except Exception as e:  # noqa
        log_error("/users['GET']", e.args, type(e).__name__, e)
        abort(500)


@user_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_single_user(user_id):
    """
    Retrieves a single user from storage based on their
    user ID and returns the user's information in JSON format.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    try:
        return js(user.to_dict())    
    except Exception as e:
        log_error('/users/<user_id>', e.args, type(e).__name__, e)
        abort(500)
    

@user_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    deletes a user from storage based on their user ID.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    try:
        user.delete()
        storage.save()
        return js({}), 204
    except Exception as e:
        abort(500)


@user_views.route("/users", methods=["POST"], strict_slashes=False)
def create_new_user():
    """
    creates a new user by extracting data from a
    JSON request, hashing, the password, creating a
    new User instance, and saving it to storage.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    parse_dict(data, ["email", "password", "first_name", "last_name"],
               status_code=400)
    
    if storage.exist(data["email"]):
        abort(409, "User exists")

    if validate_password(data.get("password", None)):
        data["password"] = md5(data.pop("password", None).encode()).hexdigest()

    try:
        instance = User(**data)
        instance.save()
        return js(instance.to_dict()), 201
    except Exception as e:  # noqa
        abort(500)


@user_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    updates a user's information in a storage system,
    including hashing the password if provided.
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    data.pop("email", None)

    if validate_password(data.get("password", None)):
        data["password"] = md5(data.pop("password", None).encode()).hexdigest()

    for key, value in data.items():
        setattr(user, key, value)

    try:
        user.save()
        return js(user.to_dict()), 200
    except Exception as e:
        abort(500)
