# Flask Blog API
## T2A2 Webserver

<br> 


# How To Run The Blog Api

The blog api has been deployed to Render with the base url:
- "https://blog-api.theomarentes.dev/"

All endpoints are documented in this README document.

<br>

To run from local machine (postgresql):
1. Create a new postgresql user and give permissions
2. Create a postgresql database (blog_api)
3. Edit ".env" file so "SQL_DATABASE_URI" matches user and database details
4. Start python virtual invironment (python3 -m venv venv)
5. Activate virtual environment (source venv/bin/activate)
6. Install requirements (pip install -r requirements.txt)
7. Create and seed tables (flask db drop && flask db create && flask db seed)
8. Run flask app (flask run)

<div style="page-break-after: always"></div>

# Identification of the problem being solved by building a blog api
Utilizing the blog API solves a number of problems related to development, scalability and blog management. 
- The blog API allows users to create cross-platform blog websites quickly and securely.
- The API simplifies content management - it allows users to create, read, update and delete blog posts programmatically.
- With the API, cross-platform applications can be created seamlessly using the same data.
- As the blog grows, the API scales without issue, allowing for high traffic and content volume.
- The API has strong security, solving the problem of authentication in a blog environment.

<div style="page-break-after: always"></div>

# Why is it a problem that needs solving?
The problems outlined above are prominent issues that need solving.
- Users access blogs from various devices and platforms, and manually developing separate interfaces for each is time-consuming and costly. The blog API streamlines cross-platform development, ensuring consistent user experiences and saving significant development resources.
- Manually managing blog content can be inefficient and error-prone. An API automates content management, reducing human errors, saving time, and allowing bloggers to focus on creating content rather than administrative tasks.
- Building separate applications for different platforms increases development complexity and maintenance efforts. A Blog API provides a unified data source, allowing developers to create cross-platform applications that share data seamlessly, simplifying development and maintenance.
- As a blog gains popularity, it must handle increased traffic and content volume. Manually scaling infrastructure can lead to downtime and performance issues. A scalable Blog API can grow with the blog, ensuring a smooth user experience and accommodating spikes in traffic without disruptions.
- Blogs often contain valuable content and user data, making them attractive targets for cyberattacks. Weak authentication and authorization systems can lead to data breaches. A secure Blog API offers robust authentication and access control, protecting content and user information from unauthorized access and cyber threats.

<div style="page-break-after: always"></div>

<div style="page-break-after: always"></div>

# Documentation of all endpoints

## Auth Endpoints

### POST "/auth/register" 
- Registers a new user to the blog and logs in. Returns authentication token.

- Request body:
  
   {

         "name": "...",

         "email": "...",

         "password": "..."

   }


- Validations:
  - "name" is required, must be between 1-50 characters and must contain only letters, numbers, spaces or dashes.
  - "email" is required, must be unique, between 6-40 characters and must be an email address.
  - "password" is required, must be at least 8 characters and must contain an upper-case character, a symbol and a number. 


- Response:
  - { "token": access_token }

<br>

<div style="page-break-after: always"></div>

### POST "/auth/login" 
- Allows a user to log in to the blog. Returns authentication token.

- Request body:
  
   {

         "email": "...",

         "password": "..."

   }


- Response:
  - { "token": access_token }


<br>

<div style="page-break-after: always"></div>

## Posts Endpoints

### GET "/posts"
- Returns all posts with all related information. This endpoint would be useful for creating a blog website from one endpoint.
- Response is a list of blog posts:
```json
   [   
      {
        "author_info": {
            "follower_count": 2,
            "name": "Jim Parsons",
            "user_id": 1
        },
        "categories": [
            "TV"
        ],
        "comments": [
            {
                "author_info": {
                    "name": "Lebron James",
                    "user_id": 2
                },
                "comment_id": 1,
                "comment_text": "Wow this is fascinating!",
                "like_count": 1
            }
        ],
        "like_count": 2,
        "post_content": "My journey on...",
        "post_title": "My Experience With The Big Bang Theory"
      },
      {
         ...
      }
   ]
```

<br>
<div style="page-break-after: always"></div>
(Posts Endpoint)

### GET "/posts/compact"
- Returns a compact list of all posts, showing only the author, title and post_id.
- Response is a compact list of blog posts:
```json
[
    {
        "author_info": {
            "name": "Jim Parsons",
            "user_id": 1
        },
        "post_id": 1,
        "post_title": "My Experience With The Big Bang Theory"
    },
    {
        "author_info": {
            "name": "Lebron James",
            "user_id": 2
        },
        "post_id": 2,
        "post_title": "Playing For The Lakers"
    }
]
```
<br>

<div style="page-break-after: always"></div>
(Posts Endpoint)

### GET "/posts/<post_id>"
- Allows the user to view a blog post by post_id. 
- Response is one blog post.
```json
[
    {
        "author_info": {
            "follower_count": 2,
            "name": "Jim Parsons",
            "user_id": 1
        },
        "categories": [
            "TV"
        ],
        "comments": [
            {
                "author_info": {
                    "name": "Lebron James",
                    "user_id": 2
                },
                "comment_id": 1,
                "comment_text": "Wow this is fascinating!",
                "like_count": 1
            }
        ],
        "like_count": 2,
        "post_content": "My journey on...",
        "post_title": "My Experience With The Big Bang Theory"
    }
]
```

<br>
<div style="page-break-after: always"></div>
(Posts Endpoint)

### GET "/posts/category/<category_name>"
- Allows a user to view posts by category name (string).
- Response is a list of blog posts:
e.g. "/posts/category/sports"
```json
[
    {
        "author_info": {
            "follower_count": 1,
            "name": "Lebron James",
            "user_id": 2
        },
        "categories": [
            "Sports"
        ],
        "comments": [
            {
                "author_info": {
                    "name": "Christiano Ronaldo",
                    "user_id": 3
                },
                "comment_id": 2,
                "comment_text": "Amazing post, thank you Lebron.",
                "like_count": 1
            }
        ],
        "like_count": 1,
        "post_content": "Playing for the...",
        "post_title": "Playing For The Lakers"
    },
    {
      ...
    }
]
```
<br>
<div style="page-break-after: always"></div>
(Posts Endpoint)

### POST "/posts/" 
- Allows the user to create a new blog post. Requires authentication.

- Request body:
  
   {

         "post_title": "...",

         "post_content": "...",

         "categories": "..."

   }


- Validations:
  - "post_title" is required. It must be less than 50 characters
  - "post_content" is required. It must be less than 5000 characters
  - "categories" is optional. It must be a string or a list of strings

- Response:
  - {"message": "new blog post created successfully.", "post_id": post_id}

<br>
<div style="page-break-after: always"></div>
(Posts Endpoint)

### PUT "/posts/<post_id>"
- Allows the user to update a blog post. Requires authentication.

- Request body:
  
   {

         "post_title": "...",

         "post_content": "..."

   }


- Validations:
  - "post_title" is required and must be less than 50 characters
  - "post_content" is required and must be less than 5000 characters

- Response:
  - {"message": "post updated successfully.", "post_id": post_id}

<br>


### DELETE "/posts/<post_id>"
- Allows the user to delete a blog post by post_id

- Response:
  - {"message": "post deleted successfully.", "post_id": post_id}


<br>

<div style="page-break-after: always"></div>

## Users Endpoints

### GET "/users"
- Returns information about all users. Only the user_id, name, email and followers are shown.

- Response is a list of users:
```json
[
    {
        "email": "jimparsons@gmail.com",
        "followers": [
            {
                "follow_id": 2,
                "follower_id": 3
            }
        ],
        "name": "Jim Parsons",
        "user_id": 1
    },
    {
      ...
    }
]
```

<div style="page-break-after: always"></div>


### GET "/users/<user_id>"
- Returns information about a particular user by user_id. This endpoint displays the user's name, email, follower_count, followers, likes and blog posts.

- Response is one user:
```json
{
    "blog_posts": [
        {
            "post_id": 1,
            "post_title": "My Experience With The Big Bang Theory"
        }
    ],
    "email": "jimparsons@gmail.com",
    "follower_count": 2,
    "followers": [
        {
            "follow_id": 2,
            "follower_id": 3
        }
    ],
    "likes": [
        {
            "like_id": 1,
            "post_id": 2
        }
    ],
    "name": "Jim Parsons"
}
```

<br>

<div style="page-break-after: always"></div>

### GET "/users/posts/<user_id>"
- View a user's blog posts by user_id.

- Response is a list of blog posts:
```json
{
    "blog_posts": [
        {
            "like_count": 2,
            "post_content": "My journey...",
            "post_id": 1,
            "post_title": "My Experience With The Big Bang Theory",
            "posted_date": "2012-12-12T00:00:00",
            "updated_date": "2014-08-10T00:00:00"
        },
        {
         ...
        }
    ]
}
```

<div style="page-break-after: always"></div>

### GET "/users/comments/<user_id>"
- View a user's comments by user_id.

- Response is a list of comments:
```json
{
    "comments": [
        {
            "comment_date": "2017-10-01T00:00:00",
            "comment_id": 3,
            "comment_text": "Your family is beautiful!",
            "like_count": 1,
            "post_id": 3,
            "updated_date": "2018-01-02T00:00:00"
        },
        {
            "comment_date": "2015-11-02T00:00:00",
            "comment_id": 6,
            "comment_text": "Lovely family!",
            "like_count": 1,
            "post_id": 4,
            "updated_date": "2016-11-04T00:00:00"
        }
    ]
}
```
<div style="page-break-after: always"></div>

### GET "/users/likes/<user_id>"
- View a user's likes by user_id.

- Response is a list of likes:
```json
{
    "likes": [
        {
            "like_id": 1,
            "post_id": 2
        },
        {
            "like_id": 2,
            "post_id": 3
        },
        {
            "comment_id": 3,
            "like_id": 3
        }
    ]
}
```

<div style="page-break-after: always"></div>

### PUT "/users"
- Update user's details. Requires authentication.

- Request body:
  
   {

         "name": "...",

         "email": "...",

         "password": "..."

   }


- Validations:
  - At least 1 piece of information must be updated. Only 1 field is required.
  - "name" must be between 1-50 characters and must contain only letters, numbers, spaces or dashes.
  - "email" must be unique, between 6-40 characters and must be an email address.
  - "password" must be at least 8 characters and must contain an upper-case character, a symbol and a number. 

- Response:
  - {"message": "updated user details"}


<div style="page-break-after: always"></div>



## Comments Endpoints

### GET "/comments/<post_id>"
- View the comments on a blog post by post_id.

- Response is a list of comments:
```json
{
    "comments": [
        {
            "author_info": {
                "name": "Lebron James"
            },
            "comment_date": "2013-12-12T00:00:00",
            "comment_id": 1,
            "comment_text": "Wow this is fascinating!",
            "like_count": 1,
            "updated_date": "2014-05-10T00:00:00"
        },
        {
            "author_info": {
                "name": "Christiano Ronaldo"
            },
            "comment_date": "2017-10-02T00:00:00",
            "comment_id": 4,
            "comment_text": "I love this show!",
            "like_count": 0,
            "updated_date": "2019-11-07T00:00:00"
        }
    ]
}
```
<div style="page-break-after: always"></div>

### POST "/comments/<post_id>"
- Post a comment on a blog post by post_id. Requires authentication.

- Request body:
  
   {

         "comment_text": "..."

   }


- Validations:
  - "comment_text" is required and must be less than 500 characters.

- Response:
  - {"message": "new comment created successfully.", "comment_id": comment_id}


<div style="page-break-after: always"></div>

### PUT "/comments/<comment_id>"
- Edit a comment by comment_id. Requires authentication.

- Request body:
  
   {

         "comment_text": "..."

   }


- Validations:
  - "comment_text" is required and must be less than 500 characters.

- Response:
  - {"message": "comment updated successfully.", "comment_id": comment_id}


<br>

### DELETE "/comments/<comment_id>"
- Delete a comment by comment_id.

- Response:
  - {"message":"comment deleted successfully", "comment_id": f"{comment_id}"}



<div style="page-break-after: always"></div>

## Categories Endpoints

### POST "/category/<post_id>"
- Add a new category to a blog post. Requires authentication.

- Request body:
  
   {

         "category": "..."

   }


- Validations:
  - "category" is required and must be a string.

- Response:
  - {"message": "New category added successfully.", "post_id": post_id}



<div style="page-break-after: always"></div>

### DELETE "/category/<post_id>"
- Delete a category from a blog post. Requires authentication.

- Request body:
  
   {

         "category": "..."

   }


- Validations:
  - "category" is required and must be a string.

- Response:
  - {"message":"category deleted successfully", "post_id": post_id}



<div style="page-break-after: always"></div>

## Followers Endpoints

### POST "/followers/<user_id>"
- Follow a user by user_id. Requires authentication.

- Response:
  - {"message": "Followed user {user_id} successfully.", "follow_id": follow_id}


<br>

### DELETE "/followers/<user_id>"
- Unfollow a user by user_id. Requires authentication.

- Response:
  - {"message": "unfollowed successfully", "follow_id": "follow_id }

<div style="page-break-after: always"></div>

### GET "/followers/<user_id>"
- Get a list of a user's followers by user_id.

- Response is a list of followers:
```json
{
    "followers": [
        {
            "follow_id": 2,
            "follower_id": 3,
            "follower_name": "Christiano Ronaldo"
        },
        {
            "follow_id": 6,
            "follower_id": 4,
            "follower_name": "Joe Biden"
        }
    ]
}
```

<div style="page-break-after: always"></div>

## Likes Endpoints

### GET "/likes/post/<post_id>"
- See which users liked a blog post by post_id.

- Response is a list of likes:
```json
{
    "likers": [
        {
            "like_id": 4,
            "liker_info": {
                "name": "Lebron James",
                "user_id": 2
            }
        },
        {
            "like_id": 8,
            "liker_info": {
                "name": "Joe Biden",
                "user_id": 4
            }
        }
    ]
}
```


<div style="page-break-after: always"></div>

### GET "/likes/comment/<comment_id>"
- See which users liked a comment by comment_id.

- Response is a list of likes:
```json
{
    "likers": [
        {
            "like_id": 5,
            "liker_info": {
                "name": "Christiano Ronaldo",
                "user_id": 3
            }
        },
        {
         ...
        }
    ]
}
```

<div style="page-break-after: always"></div>

### POST "/likes/post/<post_id>"
- Allows the user to like a blog post by post_id. Requires authentication.
  
- Response:
  - { "message": "New like created successfully.", "like_id": like_id }


<br>


### POST "/likes/comment/<comment_id>"
- Allows the user to like a comment by comment_id. Requires authentication.
  
- Response:
  - { "message": "New like created successfully.", "like_id": like_id }


<br>

### DELETE "/likes/post/<post_id>"
- Allows the user to remove a like from a blog post by post_id. Requires authentication.
  
- Response:
  - {"message":"like deleted successfully", "like_id": like_id}

<br>


### DELETE "/likes/comment/<comment_id>"
- Allows the user to remove a like from a comment by comment_id. Requires authentication.
  
- Response:
  - {"message":"like deleted successfully", "like_id": like_id}


<br>

<div style="page-break-after: always"></div>

## Third party services
Multiple third party services will be used in the application.
| Service         | Description |
| --------------- | ----------- |
| Flask           | Micro web framework for Python used to build web applications. Provides tools and libraries for handling web requests, routing, and other web-related tasks |
| PostgreSQL      | Powerful, open-source relational database management system known for its ACID compliance and support for complex data types |
| SQLAlchemy      | Python library that provides an Object-Relational Mapping (ORM) toolkit, allowing developers to interact with databases using Python objects instead of writing raw SQL queries |
| Marshmallow     | An extension for Flask that integrates the Marshmallow library, enabling easy serialization and deserialization of complex data types for use in web APIs |
| Bcrypt          | A password-hashing function commonly used for securely storing passwords in databases. Adds a layer of security by hashing passwords to protect against brute-force and rainbow table attacks |
| JSON Web Tokens | The Flask JWT Extended extension simplifies the integration of JSON Web Tokens (JWTs) for user authentication and authorization in Flask applications |
| Psycopg2        | A PostgreSQL adapter for Python that allows Python applications to connect to and interact with PostgreSQL databases |
| dotenv          | A library for loading environment variables from a .env file into the application's environment, making it easier to configure settings and sensitive information |

<div style="page-break-after: always"></div>


<div style="page-break-after: always"></div>

