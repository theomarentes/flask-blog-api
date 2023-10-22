from controllers.users_controllers import users
from controllers.blog_posts_controllers import blog_posts
from controllers.comments_controllers import comments
from controllers.auth_controllers import auth
from controllers.likes_controllers import likes
from controllers.followers_controllers import  followers
from controllers.categories_controllers import category


registered_controllers = (
    users,
    blog_posts,
    comments,
    auth,
    likes,
    followers,
    category
)