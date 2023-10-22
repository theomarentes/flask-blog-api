from main import db

class Like(db.Model):
    # define the name of the database table associated with this model
    __tablename__ = "likes"

    # unique identifier for each like
    like_id = db.Column(db.Integer, primary_key=True)

    # ID of the user who performed the like (foreign key to the "users" table)
    liker_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # ID of the blog post that was liked (foreign key to the "blogposts" table)
    post_id = db.Column(db.Integer, db.ForeignKey("blogposts.post_id"))

    # ID of the comment that was liked (foreign key to the "comments" table)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.comment_id"))

    # establish a relationship with the user who performed the like (overlaps with "likes" relationship in User model)
    liker_info = db.relationship(
        "User",
        overlaps="likes"
    )