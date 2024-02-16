#!/usr/bin/python3

"""
Models for the routes of the User_views
"""


from flask import abort, request
from hashlib import md5
from json import dumps as js
from api.v1.views import user_views
from models import storage
from utils.validators import pop_dict
from models.user import User
from utils.validators import parse_dict, validate_password
from utils.error import log_error


@user_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    Retrieves all users from storage and returns a list
    of their dictionaries.

    Returns:
        A JSON response containing a list of dictionaries representing all users.
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

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        A JSON response containing the user's information.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    try:
        return js(user.to_dict())
    except Exception as e:
        log_error("/users/<user_id>", e.args, type(e).__name__, e)
        abort(500)


@user_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user from storage based on their user ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        A JSON response indicating the success of the deletion.
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
    Creates a new user by extracting data from a
    JSON request, hashing the password, creating a
    new User instance, and saving it to storage.

    Returns:
        A JSON response containing the newly created user's information.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    parse_dict(data, ["email", "password", "first_name", "last_name"], status_code=400)

    if storage.exist(data["email"]):
        abort(409, "User exists")

    # if validate_password(data.get("password", None)):
    #     data["password"] = md5(data.pop("password", None).encode()).hexdigest()

    try:
        instance = User(**data)
        instance.save()
        return js(instance.to_dict()), 201
    except Exception as e:
        abort(500)


@user_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates a user's information in a storage system,
    including hashing the password if provided.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        A JSON response containing the updated user's information.
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    data = pop_dict(data, ["__class__", "id", "created_at", "updated_at"])

    for key, value in data.items():
        setattr(user, key, value)

    try:
        user.save()
        return js(user.to_dict()), 200
    except Exception as e:
        abort(500)


@user_views.route("/users/login", methods=["POST"], strict_slashes=False)
def login_user():
    """
    Logs in a user by checking the provided email and password
    against the stored user data.

    Returns:
        A JSON response indicating the success of the login.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    res = request.get_json()
    parse_dict(res, ["email", "password"], status_code=400)

    user, passwd = storage.exist(res["email"], data=True)

    if not user:
        abort(402, "Invalid email")

    if validate_password(res["password"]):
        if passwd != res["password"]:
            abort(401, "Invalid password")
    else:
        abort(400, "Invalid password")

    user = pop_dict(user, ["__class__", "created_at", "updated_at"])
    try:
        return js(user), 200
    except Exception as e:
        abort(500)


@user_views.route("/users/validate", methods=["GET"], strict_slashes=False)
def validate_user_email():
    """
    validates user by email checking the provided email
    against the stored user data.

    Returns:
        A JSON response indicating the success of the login.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    res = request.get_json()
    parse_dict(res, ["email"], status_code=400)


    if "data" in res:
        user = storage.exist(res["email"], data=True)
    else:
        user = storage.exist(res["email"])
        user = {"response": user}

    try:
        return js(user), 200
    except Exception as e:
        abort(500)