# import Regex, SQLAlchemy and BCrypt
import re
from main import db, bcrypt

# flask related imports for requests, responses and authentication
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# import exception handling
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

# import models
from models.users import User
from models.likes import Like
from models.followers import Follower
from models.comments import Comment

# import schemas
from schemas.users import user_schema, users_schema, UserSchema
from schemas.comments import CommentSchema
from schemas.likes import likes_schema, LikeSchema


users = Blueprint("users", __name__, url_prefix="/users")


# validation error handler - catches validation errors and outputs the error
@users.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error - `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@users.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({'error': e.description}), 400


# key error handler - occurs when keys are missing from request
@users.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The {e} field is required'}), 400


# GET "/users"
# list of all users (compact view)
@users.route("/", methods=["GET"])
def get_users():
    # query all users from the User table
    stmt = db.select(User)
    users = db.session.scalars(stmt)

    # define the schema to filter and structure the user data
    filtered_schema = UserSchema(many=True, only=("user_id", "name", "email", "follower_count"))

    # dump and filter user data based on the schema
    filtered = filtered_schema.dump(users)

    # iterate through the filtered users to calculate and update follower counts
    for user in filtered:
        # query the Follower table to count followers for each user
        user["follower_count"] = db.session.query(Follower).filter_by(followed_id=user["user_id"]).count()
        
    return jsonify({"users": filtered }), 200

# GET "/users/<user_id>"
# view user details by user_id (detailed view)
@users.route("/<int:user_id>", methods=["GET"])
def view_user(user_id: int):
    # query the User table to get user details based on user_id
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    # calculate and update the user's follower count by querying the Follower table
    user.follower_count = db.session.query(Follower).filter_by(followed_id=user_id).count()

    # define the schema to filter and structure the user data
    filtered_schema = UserSchema(only=("name", "email", "follower_count", "followers", "likes.like_id", "likes.post_id", "likes.comment_id", "blog_posts.post_title", "blog_posts.post_id"))

    # dump and filter user data based on the schema
    json = filtered_schema.dump(user)

    # iterate through the user's likes and remove null values for comment_id and post_id
    for like in json["likes"]:
        if like["comment_id"] is None:
            del like["comment_id"]
        if like["post_id"] is None:
            del like["post_id"]

    return jsonify(json), 200


# GET "/users/posts/<user_id>"
# view a user's posts by user_id
@users.route("/posts/<int:user_id>", methods=["GET"])
def view_user_posts(user_id: int):
    # query the User table to get user details based on user_id
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        return(jsonify({"error": "user does not exist"})), 400

    # calculate and update the user's follower count by querying the Follower table
    user.follower_count = db.session.query(Follower).filter_by(followed_id=user_id).count()

    # iterate through the user's blog posts and calculate the like count for each post
    for post in user.blog_posts:
        post.like_count = db.session.query(Like).filter_by(post_id=post.post_id).count()

    # define the schema to filter and structure the user's blog post data
    filtered_schema = UserSchema(only=("blog_posts.updated_date", "blog_posts.posted_date", "blog_posts.post_title", "blog_posts.post_id", "blog_posts.post_content", "blog_posts.like_count"))

    # dump and filter the user's blog post data based on the schema
    return jsonify(filtered_schema.dump(user)), 200


# GET "/users/comments/<user_id>"
# view a user's comments by user_id
@users.route("/comments/<int:user_id>", methods=["GET"])
def view_user_comments(user_id: int):
    # query the Comment table to get comments authored by the user based on user_id
    stmt = db.select(Comment).filter_by(author_id=user_id)
    comments_scalars = db.session.scalars(stmt)

    # define the schema to filter and structure the user's comment data
    filtered_schema = CommentSchema(many=True, only=("comment_id", "comment_text", "comment_date", "updated_date", "post_id", "like_count"))

    # dump and filter the user's comment data based on the schema
    comments = filtered_schema.dump(comments_scalars)

    # calculate and update the like count for each comment
    for comment in comments:
        comment["like_count"] = db.session.query(Like).filter_by(comment_id=comment["comment_id"]).count()

    # return the user's comments with their updated like counts
    return jsonify({"comments": comments}), 200


# GET "/users/likes/<user_id>"
# view a user's liked posts by user id
@users.route("/likes/<int:user_id>", methods=["GET"])
def view_user_likes(user_id: int):
    # query the Like table to get likes by the user based on user_id
    stmt = db.select(Like).filter_by(liker_id=user_id)
    likes_scalars = db.session.scalars(stmt)

    # define the schema to filter and structure the user's like data
    filtered_schema = LikeSchema(many=True, only=("comment_id", "like_id", "post_id"))

    # dump and filter the user's like data based on the schema
    likes = filtered_schema.dump(likes_scalars)

    # clean up the response by removing None values for comment_id or post_id
    for like in likes:
        if like["comment_id"] == None:
            del like["comment_id"]
        elif like["post_id"] == None:
            del like["post_id"]

    # return the user's likes with cleaned-up data
    return jsonify({"likes": likes}), 200


# PUT "/users"
# update logged in user details - requires authentication
@users.route("/", methods=["PUT"])
@jwt_required()
def update_post():
    # get the user's ID from the JWT token
    id = get_jwt_identity()

    # query the User table to get the user based on user_id
    stmt = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(stmt)

    # get the updated user information from the request JSON
    user_fields = request.json

    # check if at least one of 'name', 'email', or 'password' fields is provided
    if "name" not in user_fields and "email" not in user_fields and "password" not in user_fields:
        return jsonify({'error': 'The \'name\', \'email\' or \'password\' field is required'}), 400

    # update the user's name if provided in the request
    if "name" in user_fields:
        user.name = user_fields["name"]

    # update the user's email if provided in the request
    if "email" in user_fields:
        user.email = user_fields["email"]

    # update the user's password if provided in the request
    if "password" in user_fields:
        # define a password pattern and check if the new password matches it
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^\.&*-]).{8,}$"
        if re.match(pattern, user_fields["password"]) is None:
            return jsonify({'error': 'The \'password\' field must be at least 8 characters and must contain an upper-case character, a symbol, and a number.'}), 403
        # hash and store the new password
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    # commit the changes to the database
    db.session.commit()

    # return a success message
    return jsonify({"message": "updated user details"}), 200
