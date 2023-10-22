from main import db

class Comment(db.Model):
    # define the name of the database table
    __tablename__ = "comments"

    # define the columns of the comment table
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False)  # unique identifier for the comment
    comment_text = db.Column(db.Text, nullable=False)  # text content of the comment
    comment_date = db.Column(db.DateTime, nullable=False)  # date and time when the comment was created
    updated_date = db.Column(db.DateTime)  # date and time when the comment was last updated (nullable)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)  # ID of the comment author
    post_id = db.Column(db.Integer, db.ForeignKey("blogposts.post_id"), nullable=False)  # ID of the associated blog post
    like_count = db.Column(db.Integer)  # count of likes received by this comment

    # define a relationship with the User model to retrieve comment author information
    author_info = db.relationship(
        "User",
        overlaps="comments"
    )
