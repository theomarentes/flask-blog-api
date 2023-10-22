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
from models.blog_posts import BlogPost
from models.likes import Like
from models.followers import Follower
from models.users import User
from models.categories import Category

# import schemas
from schemas.blog_posts import blogpost_schema, blogposts_schema, BlogPostSchema
from schemas.categories import category_schema


blog_posts = Blueprint("blogposts", __name__, url_prefix="/posts")


# validation error handler - catches validation errors and outputs the error
@blog_posts.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation Error - `{e}`"}), 403


# bad request error handler - occurs when invalid POST requests are sent
@blog_posts.errorhandler(BadRequest)
def bad_request_error(e):
    return jsonify({'error': e.description}), 400


# key error handler - occurs when keys are missing from request
@blog_posts.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The {e} field is required'}), 400


# GET "/posts"
# view complete list of blog posts
@blog_posts.route("/", methods=["GET"])
def get_posts():
    # query all blog posts from the database
    stmt = db.select(BlogPost)
    posts = db.session.scalars(stmt)

    # define an empty list to append serialized posts
    serialized_posts = []
    
    # define a schema to filter and serialize the post data
    filtered_schema = BlogPostSchema(
        only=(
            "post_content",
            "like_count",
            "post_title",
            "post_id",
            "author_info.follower_count",
            "author_info.name",
            "author_info.user_id",
            "categories",
            "comments.author_info.name",
            "comments.author_info.user_id",
            "comments.comment_id",
            "comments.comment_text",
            "comments.like_count"
        )
    )

    for post in posts:
        # calculate and set the like count for each post
        like_count = db.session.query(Like).filter_by(post_id=post.post_id).count()
        post.like_count = like_count
        
        # calculate and set the follower count for each post's author
        follower_count = db.session.query(Follower).filter_by(followed_id=post.author_id).count()
        post.author_info.follower_count = follower_count

        for comment in post.comments:
            # calculate and set the like count for each comment
            like_count = db.session.query(Like).filter_by(comment_id=comment.comment_id).count()
            comment.like_count = like_count
            
            # get and set the author's name for each comment
            author_name = db.session.query(User).filter_by(user_id=comment.author_id).first()
            comment.author_name = author_name.name
        
        # serialize the post data using the filtered schema and append to the list
        serialized_post = filtered_schema.dump(post)
        serialized_posts.append(serialized_post)
    
    # return the serialized posts as JSON
    return jsonify(serialized_posts), 200


# GET "/posts/compact"
# view a compact list of posts (titles and ID)
@blog_posts.route("/compact", methods=["GET"])
def get_posts_list():
    # query all blog posts from the database
    stmt = db.select(BlogPost)
    posts = db.session.scalars(stmt)
    
    # define a schema to filter and serialize the post data (compact view)
    filtered_schema = BlogPostSchema(
        many=True,  # indicating that we are serializing multiple posts
        only=("post_title", "author_info.user_id", "author_info.name", "post_id")
    )
    
    # serialize the post data using the filtered schema and return as JSON
    return jsonify(filtered_schema.dump(posts)), 200


# GET "/posts/<post_id>"
# view a single blog post by 'post_id'
@blog_posts.route("/<int:post_id>", methods=["GET"])
def view_post(post_id: int):
    # query the blog post with the given post_id from the database
    stmt = db.select(BlogPost).filter_by(post_id=post_id)
    post = db.session.scalar(stmt)

    # if the post doesn't exist return a 404 error
    if not post:
        return jsonify({'error': f'post with ID {post_id} not found.'}), 404
    
    # initialize a list to hold serialized posts
    serialized_posts = []
    
    # define a schema to filter and serialize the post data (detailed view)
    filtered_schema = BlogPostSchema(
        only=("post_content", "like_count", "post_title", "author_info.follower_count",
              "author_info.name", "author_info.user_id", "categories",
              "comments.author_info.name", "comments.author_info.user_id",
              "comments.comment_id", "comments.comment_text", "comments.like_count")
    )
    
    # calculate the like count for the post
    like_count = db.session.query(Like).filter_by(post_id=post.post_id).count()
    post.like_count = like_count
    
    # calculate the follower count for the post's author
    follower_count = db.session.query(Follower).filter_by(followed_id=post.author_id).count()
    post.author_info.follower_count = follower_count
    
    # iterate through comments to calculate like counts and author names
    for comment in post.comments:
        like_count = db.session.query(Like).filter_by(comment_id=comment.comment_id).count()
        comment.like_count = like_count
        author_name = db.session.query(User).filter_by(user_id=comment.author_id).first()
        comment.author_name = author_name.name
    
    # serialize the post data using the filtered schema and append it to the list
    serialized_post = filtered_schema.dump(post)
    serialized_posts.append(serialized_post)
    
    # return the serialized post data as JSON
    return jsonify(serialized_posts), 200


# GET "/posts/category/<category_name>"
# view posts by category name
@blog_posts.route("/category/<category_name>", methods=["GET"])
def view_category(category_name):
    # query all blog posts from the database
    stmt = db.select(BlogPost)
    posts = db.session.scalars(stmt)
    
    # initialize a list to store posts that belong to the specified category
    category_posts = []
    
    # loop through all blog posts and their associated categories
    for post in posts:
        for category in post.categories:
            # check if the lowercase category name matches the requested category name
            if category_name.lower() in category.category_name.lower():
                # if it matches, add the post to the category_posts list and break the loop
                category_posts.append(post)
                break
        
    # define a schema to filter and serialize the post data (detailed view)
    filtered_schema = BlogPostSchema(
        only=("post_content", "like_count", "post_title", "author_info.follower_count",
              "author_info.name", "author_info.user_id", "categories",
              "comments.author_info.name", "comments.author_info.user_id",
              "comments.comment_id", "comments.comment_text", "comments.like_count")
    )
    
    # initialize a list to store serialized post data
    serialized_posts = []
    
    # iterate through posts in the specified category
    for post in category_posts:
        # calculate the like count for the post
        like_count = db.session.query(Like).filter_by(post_id=post.post_id).count()
        post.like_count = like_count
        
        # calculate the follower count for the post's author
        follower_count = db.session.query(Follower).filter_by(followed_id=post.author_id).count()
        post.author_info.follower_count = follower_count
        
        # iterate through comments to calculate like counts and author info
        for comment in post.comments:
            like_count = db.session.query(Like).filter_by(comment_id=comment.comment_id).count()
            comment.like_count = like_count
            author_info = db.session.query(User).filter_by(user_id=comment.author_id).first()
            comment.author_info = author_info
        
        # serialize the post data using the filtered schema and append it to the list
        serialized_post = filtered_schema.dump(post)
        serialized_posts.append(serialized_post)
    
    # return the serialized post data as JSON
    return jsonify(serialized_posts), 200


# POST "/posts"
# create a new blog post - requires authentication
@blog_posts.route("/", methods=["POST"])
@jwt_required()
def create_post():
    # get the user's identity (user_id) from the JWT token
    id = get_jwt_identity()
    q = db.select(User).filter_by(user_id=id)
    user = db.session.scalar(q)
    
    # load the JSON data from the request into the post_json variable
    post_json = (request.json)
    
    # add author_id, posted_date, updated_date, and initial like_count to the post_json
    post_json["author_id"] = id
    post_json["posted_date"] = datetime.now()
    post_json["updated_date"] = datetime.now()
    post_json["like_count"] = 0
 
    # check if 'categories' field is in post_json and handle it
    categories = []
    if "categories" in post_json:
        categories = post_json["categories"]
        del post_json["categories"]

    # check for the presence and length of 'post_title' and 'post_content' fields
    if "post_title" not in post_json:
        return jsonify({'error': 'The \'post_title\' field is required'}), 400
    elif len(post_json["post_title"]) > 50:
        return jsonify({'error': '\'post_title\' must be less than 50 characters'}), 403
    if "post_content" not in post_json:
        return jsonify({'error': 'The \'post_content\' field is required'}), 400
    elif len(post_json["post_content"]) > 5000:
        return jsonify({'error': '\'post_content\' must be less than 5000 characters'}), 403
    
    # load the post_json data into a BlogPostSchema
    post_json = blogpost_schema.load(post_json)
    
    # create a BlogPost object with the loaded data
    post = BlogPost(**post_json)
    
    # add the new post to the database
    db.session.add(post)
    
    # commit the changes to the database
    db.session.commit()
    
    # handle categories if provided
    if categories:
        # check if categories provided is a list
        if type(categories) == list:
            for each in categories:
                if type(each) == str:
                    category = Category()
                    category.category_name = each
                    category.post_id = post.post_id
                    db.session.add(category)
                else:
                    return jsonify({'error': '\'categories\' list must contain strings'}), 403
        elif type(categories) == str:
            category = Category()
            category.category_name = categories
            category.post_id = post.post_id
            db.session.add(category)
        else:
            return jsonify({'error': 'The \'categories\' field must be a string or list'}), 403
        
    # commit any changes related to categories
    db.session.commit()
    
    # return a success message with the new post_id
    return jsonify({"message": "New blog post created successfully.", "post_id": post.post_id}), 200


# PUT "/posts/<post_id>"
# update a blog post - requires authentication
@blog_posts.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id: int):
    # load the JSON data from the request into the post_fields variable
    post_fields = blogpost_schema.load(request.json)

    # get the user's identity (user_id) from the JWT token
    user_id = get_jwt_identity()

    # query the User table to get the user's data
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    # query the BlogPost table to get the post that needs to be updated
    stmt = db.select(BlogPost).filter_by(post_id=post_id)
    post = db.session.scalar(stmt)

    # check if the post with the given ID exists
    if not post:
        return jsonify({'error': f'post with ID {post_id} does not exist'}), 400
    
    # check if the user attempting to update the post is the owner
    if post.author_id != user.user_id:
        return jsonify({'error': f'you are not the owner of the post with ID {post_id}'}), 401
    
    # check for the presence and length of 'post_title' and 'post_content'
    if "post_title" not in post_fields and "post_content" not in post_fields:
        return jsonify({'error': 'The \'post_title\' and/or \'post_content\' field is required'}), 400
    elif "post_title" in post_fields and len(post_fields["post_title"]) > 50:
        return jsonify({'error': '\'post_title\' must be less than 50 characters'}), 403
    elif "post_content" in post_fields and len(post_fields["post_content"]) > 5000:
        return jsonify({'error': '\'post_content\' must be less than 5000 characters'}), 403
    
    # update the post's title and content if provided in the request
    if "post_title" in post_fields:
        post.post_title = post_fields["post_title"]
    if "post_content" in post_fields:
        post.post_content = post_fields["post_content"]

    # update the post's updated_date with the current timestamp
    post.updated_date = datetime.now()

    # commit the changes to the database
    db.session.commit()

    # return a success message with the updated post_id
    return jsonify({"message": "post updated successfully", "post_id": post.post_id}), 200


# DELETE "/posts/<post_id>"
# delete a blog post - requires authentication
@blog_posts.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id: int):
    # get the user's identity (user_id) from the JWT token
    user_id = get_jwt_identity()

    # query the User table to get the user's data
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    # query the BlogPost table to get the post that needs to be deleted
    stmt = db.select(BlogPost).filter_by(post_id=post_id)
    post = db.session.scalar(stmt)

    # check if the post with the given ID exists
    if not post:
        return jsonify({'error': f'post with ID {post_id} does not exist'}), 400
    
    # check if the user attempting to delete the post is the owner
    if post.author_id != user.user_id:
        return jsonify({'error': f'you are not the owner of the post with ID {post_id}'}), 401

    # delete the post from the database
    db.session.delete(post)
    
    # commit the changes to the database
    db.session.commit()

    # return a success message with the deleted post_id
    return jsonify({"message": "post deleted successfully.", "post_id": post.post_id}), 200