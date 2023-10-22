from main import ma
from marshmallow import fields, validate

class CategorySchema(ma.Schema):
    
    class Meta:
        fields = "category_id", "category_name", "post_id"

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)