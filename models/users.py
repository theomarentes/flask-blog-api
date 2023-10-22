from main import db

class User(db.Model):
    # define the name of the database table associated with this model
    __tablename__ = "users"

    # unique identifier for each user
    user_id = db.Column(db.Integer, primary_key=True)

    # user's name
    name = db.Column(db.Text, nullable=False)

    # user's email address, must be unique
    email = db.Column(db.Text, nullable=False, unique=True)

    # user's hashed password
    password = db.Column(db.Text, nullable=False)

    # count of followers for this user
    follower_count = db.Column(db.Integer)

    # define a one-to-many relationship with blog posts authored by this user
    blog_posts = db.relationship(
        "BlogPost", 
        back_populates="author_info",
        cascade="all, delete"
    )

    # define a one-to-many relationship with followers (users who follow this user).
    followers = db.relationship( 
        "Follower",
        primaryjoin="User.user_id==Follower.followed_id",
        cascade="all, delete"
    )

    # define a one-to-many relationship with likes (likes created by this user).
    likes = db.relationship(
        "Like",
        primaryjoin="User.user_id==Like.liker_id",
        cascade="all, delete"
    )




