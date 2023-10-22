from main import ma
from marshmallow import fields, validate
from schemas.comments import CommentSchema
from schemas.categories import CategorySchema
from models.likes import Like

class BlogPostSchema(ma.Schema):
    # define a like_count field with a default value of 0 for loading
    like_count = fields.Integer(load_default=0)

    class Meta:
        fields = "post_id", "post_title", "post_content", "posted_date", "updated_date", "author_id", "author_info", "like_count", "categories", "comments"
        
        # specify that 'author_id' should only be loaded since 'author_info' exists
        load_only = ['author_id']

    # nested field for author information, excluding blog posts and password
    author_info = fields.Nested("UserSchema", exclude=("blog_posts", "password"))
    
    # list of nested comment fields, excluding the post_id
    comments = fields.List(fields.Nested("CommentSchema", exclude=("post_id",)))
    
    # method to retrieve categories associated with the object
    categories = fields.Method("get_categories")
    def get_categories(self, obj):
        # return a list of category names from the associated categories
        return list(category.category_name for category in obj.categories)

blogpost_schema = BlogPostSchema()
blogposts_schema = BlogPostSchema(many=True)