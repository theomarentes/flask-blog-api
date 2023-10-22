# import SQLAlchemy
from main import db

# flask related imports for requests, responses and authentication
from flask import Blueprint, jsonify, request,  abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# import exception handling
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

# import models
from models.likes import Like
from models.users import User

# import schemas
from schemas.likes import like_schema, likes_schema, LikeSchema


likes = Blueprint("likes", __name__, url_prefix="/likes")


# validation error handler - catches validation errors and outputs the error
@likes.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error - `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@likes.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({'error': e.description}), 400


# key error handler - occurs when keys are missing from request
@likes.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The {e} field is required'}), 400


# GET "/likes/post/<post_id>"
# view which users liked a blog post by post_id
@likes.route("/post/<int:post_id>", methods=["GET"])
def get_post_likes(post_id: int):
    # query the Like table to find all likes for the specified post_id
    stmt = db.select(Like).filter_by(post_id=post_id)
    likes = db.session.scalars(stmt)

    # define the schema to filter and format the like data
    filtered_schema = LikeSchema(many=True, only=("like_id", "liker_info.name", "liker_info.user_id"))

    # serialize the like data using the schema
    return jsonify({"likers": filtered_schema.dump(likes) }), 200


# GET "/likes/comment/<comment_id>"
# view which users liked a comment by comment_id
@likes.route("/comment/<int:comment_id>", methods=["GET"])
def get_comment_likes(comment_id: int):
    # query the Like table to find all likes for the specified comment_id
    stmt = db.select(Like).filter_by(comment_id=comment_id)
    likes = db.session.scalars(stmt)

    # define the schema to filter and format the like data
    filtered_schema = LikeSchema(many=True, only=("like_id", "liker_info.name", "liker_info.user_id"))

    # serialize the like data using the schema
    return jsonify({"likers": filtered_schema.dump(likes) }), 200


# POST "/likes/post/<post_id>"
# add new like to a blog post by post_id - requires authentication
@likes.route("/post/<int:post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id : int):
    # get the user's identity from the JSON Web Token
    id = get_jwt_identity()

    # query the User table to find the user based on the identity
    stmt1 = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt1)

    # query the Like table to check if the user has already liked this post
    stmt2 = db.select(Like).filter_by(liker_id=id, post_id=post_id)
    like = db.session.scalar(stmt2)

    # if a like already exists, return a message
    if like:
        return(jsonify({"error": "Like already exists."})), 400
    else:
        # if no like exists, create a new like entry
        like_json = {}
        like_json["liker_id"] = user.user_id
        like_json["post_id"] = post_id
        like = Like(**like_json)

        db.session.add(like)
        db.session.commit()
        return jsonify({"message": "New like created successfully.", "like_id": like.like_id}), 200


# POST "/likes/comment/<comment_id>"
# add new like to comment by comment_id - requires authentication
@likes.route("/comment/<int:comment_id>", methods=["POST"])
@jwt_required()
def like_comment(comment_id : int):
    # get the user's identity from the JSON Web Token
    id = get_jwt_identity()

    # query the User table to find the user based on the identity
    stmt1 = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt1)

    # query the Like table to check if the user has already liked this comment
    stmt2 = db.select(Like).filter_by(liker_id=id, comment_id=comment_id)
    like = db.session.scalar(stmt2)

    # if a like already exists, return a message
    if like:
        return(jsonify({"error": "Like already exists."})), 400
    else:
        # if no like exists, create a new like entry
        like_json = {}
        like_json["liker_id"] = user.user_id
        like_json["comment_id"] = comment_id
        like = Like(**like_json)

        db.session.add(like)
        db.session.commit()
        return jsonify({"message": "New like created successfully.", "like_id": like.like_id}), 200


# DELETE "/likes/post/<post_id>"
# remove like from post by post_id - requires authentication
@likes.route("/post/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post_like(post_id: int):
    # get the user's identity from the JSON Web Token
    user_id = get_jwt_identity()

    # query the User table to find the user based on the identity
    stmt1 = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt1)

    # query the Like table to find the like associated with the user and post
    stmt2 = db.select(Like).filter_by(post_id=post_id, liker_id=user_id)
    like = db.session.scalar(stmt2)

    # if the like doesn't exist, return an error response
    if not like:
        return(jsonify({"error": "like doesn't exist"})), 400

    # if the user is not the creator of the like, return an error response
    if like.liker_id != user.user_id:
        return(jsonify({"error": "you are not the creator of this like"})), 400

    # delete the like and commit the change to the database
    db.session.delete(like)
    db.session.commit()

    return jsonify({"message":"like deleted successfully", "like_id": f"{like.like_id}"}), 200


# DELETE "/likes/comment/<comment_id>"
# remove like from comment by comment_id - requires authentication
@likes.route("/comment/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_like(comment_id: int):
    # get the user's identity from the JSON Web Token
    user_id = get_jwt_identity()

    # query the User table to find the user based on the identity
    stmt1 = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt1)

    # query the Like table to find the like associated with the user and comment
    stmt2 = db.select(Like).filter_by(comment_id=comment_id, liker_id=user_id)
    like = db.session.scalar(stmt2)

    # if the like doesn't exist, return an error response
    if not like:
        return(jsonify({"error": "like doesn't exist"})), 400

    # if the user is not the creator of the like, return an error response
    if like.liker_id != user.user_id:
        return(jsonify({"error": "you are not the creator of this like"})), 400

    # delete the like and commit the change to the database
    db.session.delete(like)
    db.session.commit()
    
    return jsonify({"message":"like deleted successfully", "like_id": f"{like.like_id}"}), 200

