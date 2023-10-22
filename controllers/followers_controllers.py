# import SQLAlchemy
from main import db

# flask related imports for requests, responses and authentication
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# import exception handling
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

# import models
from models.followers import Follower
from models.users import User

# import schemas
from schemas.followers import follower_schema, followers_schema, FollowerSchema


followers = Blueprint("followers", __name__, url_prefix="/followers")


# validation error handler - catches validation errors and outputs the error
@followers.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error - `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@followers.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({'error': e.description}), 400


# key error handler - occurs when keys are missing from request
@followers.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The {e} field is required'}), 400


# POST "/followers/<user_id>"
# follow a user by user_id - requires authentication
@followers.route("/<int:user_id>", methods=["POST"])
@jwt_required()
def follow_user(user_id: int):
    # get the user's identity from the JWT token
    id = get_jwt_identity()

    # query the User table to get user information based on the user's ID
    stmt1 = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt1)

    # query the Follower table to check if the user is already following the specified user_id
    stmt2 = db.select(Follower).filter_by(follower_id=id, followed_id=user_id)
    follow = db.session.scalar(stmt2)
    response = follower_schema.dump(follow)

    # if the user is already following the specified user, return a message
    if response:
        return(jsonify({"error": "You already follow this user"})), 400
    # if the user is trying to follow themselves, return a message
    elif user.user_id == user_id:
        return(jsonify({"error": "You can't follow yourself"})), 400
    else:
        # create a new Follower record to represent the follow relationship
        follow_json = {}
        follow_json["follower_id"] = user.user_id
        follow_json["followed_id"] = user_id
        follow = Follower(**follow_json)

        # add the follow record to the database and commit the changes
        db.session.add(follow)
        db.session.commit()

        # return a success message with the follow_id
        return jsonify({"message": f"Followed user {user_id} successfully.", "follow_id": follow.follow_id}), 200


# DELETE "/followers/<user_id>"
# unfollow a user by user_id - requires authentication
@followers.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_post_like(user_id: int):
    # get the user's identity from the JWT token
    id = get_jwt_identity()

    # query the User table to get user information based on the user's ID
    stmt1 = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt1)

    # query the Follower table to find the follow relationship between the current user and the specified user_id
    stmt2 = db.select(Follower).filter_by(follower_id=user.user_id, followed_id=user_id)
    follow = db.session.scalar(stmt2)

    # if the follow relationship doesn't exist, return a bad request (400) with an error message
    if not follow:
        return(jsonify({"error": "this follow doesn't exist"})), 400

    # check if the current user is the creator of this follow relationship
    if follow.follower_id != user.user_id:
        return(jsonify({"error": "you are not the creator of this follow"})), 400

    # delete the follow relationship from the database and commit the changes
    db.session.delete(follow)
    db.session.commit()

    # return a success message with the follow_id
    return jsonify({"message": "unfollowed successfully", "follow_id": f"{follow.follow_id}"}), 200


# GET "/followers/<user_id>"
# get a list of followers by user_id
@followers.route("/<int:user_id>", methods=["GET"])
def get_post_likes(user_id: int):
    # query the Follower table to find all followers of the specified user_id
    stmt1 = db.select(Follower).filter_by(followed_id=user_id)
    followers = db.session.scalars(stmt1)

    # define the schema to filter and format the follower data
    filtered_schema = FollowerSchema(many=True, only=("follower_id", "follow_id"))

    # serialize the follower data using the schema
    json = filtered_schema.dump(followers)

    # iterate through each follower in the JSON data
    for follower in json:
        # query the User table to get additional information about the follower
        stmt2 = db.select(User).filter_by(user_id=follower["follower_id"])
        user = db.session.scalar(stmt2)

        # add the follower's name and user_id to the JSON data
        follower["follower_name"] = user.name
        follower["follower_id"] = user.user_id

    # return the JSON data containing the followers and their information
    return jsonify({"followers": json }), 200