from main import ma
from marshmallow import fields, validate

class LikeSchema(ma.Schema):
    class Meta:
        fields = "like_id", "liker_id", "post_id", "comment_id", "liker_info"

    # create a nested field for 'liker_info' by referencing the "UserSchema" and excluding specific fields
    liker_info = fields.Nested("UserSchema", exclude=("blog_posts", "password"))


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)