from main import ma
from marshmallow import fields, validate

class FollowerSchema(ma.Schema):
    
    class Meta:
        fields = "follow_id", "follower_id", "followed_id"

follower_schema = FollowerSchema()
followers_schema = FollowerSchema(many=True)