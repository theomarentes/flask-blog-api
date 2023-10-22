from main import db

class Follower(db.Model):
    # define the name of the database table associated with this model
    __tablename__ = "followers"

    # unique identifier for each follower relationship
    follow_id = db.Column(db.Integer, primary_key=True, nullable=False)

    # ID of the user who is following another user (foreign key to the "users" table)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # ID of the user being followed (foreign key to the "users" table)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)