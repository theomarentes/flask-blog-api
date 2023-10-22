# import SQLAlchemy
from main import db

# flask related imports for requests, responses and authentication
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# import exception handling
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

# import models
from models.categories import Category
from models.users import User
from models.blog_posts import BlogPost

# import schemas
from schemas.categories import category_schema, categories_schema
from schemas.blog_posts import blogpost_schema


category = Blueprint("category", __name__, url_prefix="/category")


# validation error handler - catches validation errors and outputs the error
@category.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error - `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@category.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({'error': e.description}), 400


# key error handler - occurs when keys are missing from request
@category.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The {e} field is required'}), 400


# POST "/category/<post_id>"
# create new category on blog post (by post_id) - requires authentication
@category.route("/<int:post_id>", methods=["POST"])
@jwt_required()
def new_category(post_id : int):
    # get the user's identity (user_id) from the JWT token
    id = get_jwt_identity()

    # query the Category table to get existing categories for the post
    stmt = db.select(Category).filter_by(post_id=post_id)
    categories = db.session.scalars(stmt)
    response = categories_schema.dump(categories)

    # query the BlogPost table to get the post by its ID
    post = db.session.query(BlogPost).get(post_id)

    # check if the post with the given ID exists
    if not post:
        return(jsonify({"error": f"post not found with ID {post_id}"})), 400

    # check if the user attempting to add a category is the owner of the post
    if str(post.author_info.user_id) != str(id):
        return(jsonify({"error": "you are not the owner of this blog post"})), 401

    # check if the requested category already exists for this post
    for category in response:
        if category["category_name"] == request.json["category"]:
            return(jsonify({"error": "category already exists."})), 400
    
    # create a new category JSON object
    category_json = {}
    category_json["category_name"] = request.json["category"]
    category_json["post_id"] = post_id
    category = Category(**category_json)

    # add the new category to the database
    db.session.add(category)
    db.session.commit()

    # return a success message with the post_id
    return jsonify({"message": "New category added successfully.", "post_id": post_id}), 200


# DELETE "/category/<post_id>"
# remove categorie on blog post (by post_id) - requires authentication
@category.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_category(post_id : int):
    # get the user's identity (user_id) from the JWT token
    id = get_jwt_identity()

    # query the BlogPost table to get the post by its ID
    post = db.session.query(BlogPost).get(post_id)

    # check if the post with the given ID exists
    if not post:
        return(jsonify({"error": f"post not found with ID {post_id}"})), 400

    # check if the user attempting to delete a category is the owner of the post
    if str(post.author_info.user_id) != str(id):
        return(jsonify({"error": "you are not the owner of this blog post"})), 401

    # query the Category table to check if the specified category exists for this post
    stmt = db.select(Category).filter_by(post_id=post_id, category_name=request.json["category"])
    category = db.session.scalar(stmt)
    response = category_schema.dump(category)

    if response:
        # if the category exists, delete it from the database
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message":"category deleted successfully", "post_id": post_id}), 200
    else:
        # if the category does not exist, return an error
        return jsonify({"error": "category does not exist"}), 400
    
    
    
    
