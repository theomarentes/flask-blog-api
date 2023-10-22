from main import ma
from marshmallow import fields, validate
from schemas.blog_posts import BlogPostSchema
from schemas.followers import FollowerSchema
from schemas.likes import LikeSchema

class UserSchema(ma.Schema):
    # define a field for user email with constraints (required, email format, length of 6-40 characters)
    email = fields.Email(
        required=True,
        validate=validate.Length(min=6, max=40, error="Email must be between 6-40 characters.")
    )

    # define a field for user name with constraints (length of 1-50 characters and must only contain letters, numbers or dashes)
    name = fields.String(
        validate=validate.And(validate.Length(min=1, max=50, error="Name must be between 1-50 characters."),
                              validate.Regexp(r'^[a-zA-Z0-9.\- ]*$', error="Name must only contain letters, numbers or dashes."))
    )

    # define a follower_count field with a default value of 0 for loading
    follower_count = fields.Integer(load_default=0)

    class Meta:
        fields = "user_id", "name", "email", "password", "blog_posts", "followers", "follower_count", "likes"
        load_only = ['password']

    # define a field for user's blog posts as a list of nested BlogPostSchema objects
    blog_posts = fields.List(fields.Nested("BlogPostSchema", exclude=("author_id",)))
    
    # define a field for user's followers as a list of nested FollowerSchema objects
    followers = fields.List(fields.Nested("FollowerSchema", exclude=("followed_id",)))
    
    # define a field for user's likes as a list of nested LikeSchema objects
    likes = fields.List(fields.Nested("LikeSchema", exclude=("liker_id",)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)