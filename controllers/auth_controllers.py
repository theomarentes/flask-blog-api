# import Regex, SQLAlchemy, BCrypt and datetime library
import re
from main import db, bcrypt
from datetime import timedelta

# flask related imports for requests, responses and authentication
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# import exception handling
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

# import models
from models.users import User

# import schemas
from schemas.users import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


# validation error handler - catches validation errors and outputs the error
@auth.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error: `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@auth.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({"error": e.description}), 400


# key error handler - occurs when keys are missing from request
@auth.errorhandler(KeyError)
def key_error(e):
    return jsonify({"error": f"The {e} field is required"}), 400


# POST "/auth/register"
# register a new user and return their json web token
@auth.route("/register", methods=["POST"])
def register_user():
    # deserialize and validate user input from the incoming JSON request
    user_fields = user_schema.load(request.json)

    # check if 'name', 'email', and 'password' fields are present in the request
    if "name" not in user_fields:
        return jsonify({"error": "The 'name' field is required"}), 400
    elif "email" not in user_fields:
        return jsonify({"error": "The 'email' field is required"}), 400
    elif "password" not in user_fields:
        return jsonify({"error": "The 'password' field is required"}), 400

    # find the user by email address
    stmt = db.select(User).filter_by(email=request.json["email"])
    user = db.session.scalar(stmt)

    # check if the user with the given email already exists
    if user:
        # return an error message if the email is already in use
        return jsonify({"error": "This email is already in use by another user"}), 400
    
    # create a new user object
    user = User()

    # set the email attribute
    user.email = user_fields["email"]

    # check that the password is a strong password using regex
    pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^\.&*-]).{8,}$"
    if re.match(pattern, user_fields["password"]) is None:
        return (
            jsonify(
                {
                    "error": "The 'password' field must be at least 8 characters and must contain an upper-case character, a symbol and a number."
                }
            ),
            403
        )
    
    # hash the password using bcrypt
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode(
        "utf-8"
    )

    # set the name of the user
    user.name = user_fields["name"]

    # add the user to the database and commit the changes.
    db.session.add(user)
    db.session.commit()

    # create a variable that sets an expiry date for the access token
    expiry = timedelta(days=1)

    # create the access token for the user
    access_token = create_access_token(identity=str(user.user_id), expires_delta=expiry)

    # return the user's access token
    return jsonify({"token": access_token}), 200


# POST "/auth/login"
# login a user with their email and password - returns their json web token
@auth.route("/login", methods=["POST"])
def login_user():
    # deserialize and validate user input from the incoming JSON request
    user_fields = user_schema.load(request.json)

    # check if 'email' is present in the deserialized user input
    if "email" not in user_fields:
        return jsonify({"error": "The 'email' field is required"}), 400

    # check if 'password' is present in the deserialized user input
    elif "password" not in user_fields:
        return jsonify({"error": "The 'password' field is required"}), 400

    # query the database to find a user with the provided email
    stmt = db.select(User).filter_by(email=request.json["email"])
    user = db.session.scalar(stmt)

    # check if a user with the provided email exists or if the password is incorrect
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return jsonify({"error": "Invalid username and/or password"}), 401

    # set the expiration time for the access token (1 day)
    expiry = timedelta(days=1)

    # create an access token for the authenticated user
    access_token = create_access_token(identity=str(user.user_id), expires_delta=expiry)

    # return the user's access token
    return jsonify({"token": access_token}), 200