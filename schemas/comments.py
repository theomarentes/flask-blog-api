from main import ma
from marshmallow import fields, validate

class CommentSchema(ma.Schema):
    # define a like_count field with a default value of 0 for loading
    like_count = fields.Integer(load_default=0)
    
    class Meta:
        fields = "comment_id", "comment_text", "comment_date", "updated_date", "author_id", "post_id", "like_count", "author_info"
    
    # nested field for author information, excluding blog posts, password and followers
    author_info = fields.Nested("UserSchema", exclude=("blog_posts", "password", "followers"))

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)