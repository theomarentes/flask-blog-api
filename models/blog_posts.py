from main import db

class BlogPost(db.Model):
    # Define the name of the database table
    __tablename__ = "blogposts"

    # define the columns of the blog post table
    post_id = db.Column(db.Integer, primary_key=True, nullable=False)  # unique identifier for the blog post
    post_title = db.Column(db.Text, nullable=False)  # title of the blog post
    post_content = db.Column(db.Text, nullable=False)  # content of the blog post
    posted_date = db.Column(db.DateTime, nullable=False)  # date when the post was created
    updated_date = db.Column(db.DateTime, nullable=False)  # date when the post was last updated
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)  # ID of the author of the post
    like_count = db.Column(db.Integer)  # count of likes on the post

    # define a relationship with the User model to retrieve author information
    author_info = db.relationship("User")

    # define a relationship with the Comment model, allowing cascade delete (when a post is deleted, its comments are deleted)
    comments = db.relationship("Comment", cascade="all, delete")

    # define a relationship with the Category model, allowing cascade delete (when a post is deleted, its categories are deleted)
    categories = db.relationship("Category", cascade="all, delete")
