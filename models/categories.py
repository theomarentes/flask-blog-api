from main import db

class Category(db.Model):
    # define the name of the database table
    __tablename__ = "categories"

    # define the columns of the category table
    category_id = db.Column(db.Integer, primary_key=True, nullable=False)  # unique identifier for the category
    category_name = db.Column(db.Text, nullable=False)  # name of the category
    post_id = db.Column(db.Integer, db.ForeignKey("blogposts.post_id"))  # ID of the associated blog post