# import SQLAlchemy and datetime library
from main import db
from datetime import date, timedelta, datetime

# flask related imports for requests, responses and authentication
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# import exception handling
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

# import models
from models.comments import Comment
from models.users import User
from models.likes import Like
from models.blog_posts import BlogPost

# import schemas 
from schemas.comments import comment_schema, comments_schema, CommentSchema



comments = Blueprint("comments", __name__, url_prefix="/comments")


# validation error handler - catches validation errors and outputs the error
@comments.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error - `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@comments.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({'error': e.description}), 400


# key error handler - occurs when keys are missing from request
@comments.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'the {e} field is required'}), 400


# GET "/comments/<post_id>"
# view all comments on a blog post (by post_id)
@comments.route("/<int:post_id>", methods=["GET"])
def get_post_comments(post_id: int):
    # query the Comment table to get all comments related to a specific post ID
    stmt = db.select(Comment).filter_by(post_id=post_id)
    comments = db.session.scalars(stmt)
    
    # define the schema for comment serialization, specifying which fields to include
    filtered_schema = CommentSchema(many=True, only=("comment_id", "comment_text", "comment_date", "like_count", "author_info.name", "author_info.user_id", "updated_date"))
    
    # serialize the comments using the specified schema
    response = filtered_schema.dump(comments)
    
    # calculate and update the like_count for each comment
    for comment in response:
        # query the Like table to count the number of likes for this comment
        q = db.select(Like).filter_by(post_id=post_id)
        comment["like_count"] = db.session.query(Like).filter_by(comment_id=comment["comment_id"]).count()
        
    # return the serialized comments
    return jsonify({"comments": filtered_schema.dump(response)}), 200


# POST "/comments/<post_id>"
# create new comment on blog post (by post_id)
@comments.route("/<int:post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id: int):
    # get the user's identity from the JWT token
    id = get_jwt_identity()

    # query the User table to get user information based on the user's ID
    stmt = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt)

    # load and validate the comment data from the request JSON
    comment_json = comment_schema.load(request.json)

    # check if 'comment_text' is present in the loaded data
    if "comment_text" not in comment_json:
        return jsonify({'error': 'The \'comment_text\' field is required'}), 400
    # check if 'comment_text' exceeds the character limit
    elif len(comment_json["comment_text"]) > 500:
        return jsonify({'error': '\'comment_text\' must be less than 500 characters'}), 403
    
    # query the BlogPost table to get the post related to the specified post_id
    post = db.session.query(BlogPost).get(post_id)

    # if the post doesn't exist, return an error message
    if not post:
        return(jsonify({"message": f"post not found with ID {post_id}"})), 400
    
    # assign the user's ID and other necessary fields to the comment JSON
    comment_json["author_id"] = user.user_id
    comment_json["post_id"] = post_id
    comment_json["comment_date"] = datetime.now()
    comment_json["updated_date"] = datetime.now()
    
    # create a new Comment object using the loaded and modified comment data
    comment = Comment(**comment_json)

    # add the comment to the database session and commit the changes
    db.session.add(comment)
    db.session.commit()
    
    # return a success message with the comment's ID
    return jsonify({"message": "new comment created successfully", "comment_id": comment.comment_id}), 200


# PUT "/comments/<comment_id>"
# update comment on blog post (by comment_id) - requires authentication
@comments.route("/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id: int):
    # load and validate the updated comment data from the request JSON
    comment_json = comment_schema.load(request.json)

    # check if 'comment_text' is present in the loaded data
    if "comment_text" not in comment_json:
        return jsonify({'error': 'The \'comment_text\' field is required'}), 400
    # check if 'comment_text' exceeds the character limit
    elif len(comment_json["comment_text"]) > 500:
        return jsonify({'error': '\'comment_text\' must be less than 500 characters'}), 403

    # get the user's identity from the JWT token
    user_id = get_jwt_identity()

    # query the User table to get user information based on the user's ID
    stmt1 = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt1)
    
    # query the Comment table to get the comment based on the specified comment_id
    stmt2 = db.select(Comment).filter_by(comment_id=comment_id)
    comment = db.session.scalar(stmt2)

    # if the comment doesn't exist, return an error message
    if not comment:
        return jsonify({'error': f'comment with ID {comment_id} does not exist'}), 400

    # check if the user is the owner of the comment
    if comment.author_id != user.user_id:
        return jsonify({'error': f'you are not the owner of the comment with ID {comment_id}'}), 401

    # update the comment's text and the 'updated_date' field
    comment.comment_text = comment_json["comment_text"]
    comment.updated_date = datetime.now()

    # commit the changes to the database
    db.session.commit()

    # return a success message with the comment's ID
    return jsonify({"message": "comment updated successfully", "comment_id": comment.comment_id}), 200


# DELETE "/comments/<comment_id>"
# remove comment on blog post (by comment_id) - requires authentication
@comments.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id: int):
    # get the user's identity from the JWT token
    user_id = get_jwt_identity()

    # query the User table to get user information based on the user's ID
    stmt1 = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt1)

    # query the Comment table to get the comment based on the specified comment_id
    stmt2 = db.select(Comment).filter_by(comment_id=comment_id)
    comment = db.session.scalar(stmt2)

    # if the comment doesn't exist, return an error message
    if not comment:
        return jsonify({'error': f'comment with ID {comment_id} does not exist'}), 400

    # check if the user is the owner of the comment
    if comment.author_id != user.user_id:
        return jsonify({'error': f'you are not the owner of the comment with ID {comment_id}'}), 401

    # delete the comment from the database
    db.session.delete(comment)
    db.session.commit()

    # return a success message with the deleted comment's ID
    return jsonify({"message": "comment deleted successfully", "comment_id": f"{comment.comment_id}"}), 200