# Corporate Microblog Service (Python Advanced Final Project)

## About this project

This repository contains a backend service for a corporate microblogging platform (similar to Twitter), implemented as a final project for a Python Advanced course.

The service provides a small but realistic REST API:

- **Authentication via `api-key` header** – each request identifies the current user by an API key.
- **Tweets** – create and delete tweets, optionally attach media files.
- **Media uploads** – upload images/files and bind them to tweets.
- **Likes** – like and unlike tweets, track how many likes each tweet has.
- **Follows** – follow and unfollow other users.
- **Feed** – get a feed of tweets from followed users, sorted by popularity (likes) and recency.
- **User profiles** – fetch information about the current user (`/users/me`) and any other user (`/users/<id>`).

The code is structured as a small production-style service: blueprints for the API, separate models and auth helpers, unified error format, and a docker-compose configuration to run the app together with PostgreSQL.

## Tech stack

- Python, Flask  
- PostgreSQL  
- SQLAlchemy, Flask-Migrate  
- Docker, docker-compose  

## Initial data / users

For simplicity users are created directly in the database or via a small helper script.

Example (Python shell):

```python
from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

user = User(name="Test user", api_key="TEST_API_KEY_123")
db.session.add(user)
db.session.commit()


Then use TEST_API_KEY_123 in the api-key header.


Example request
curl -X POST "http://localhost:5000/api/tweets" \
  -H "Content-Type: application/json" \
  -H "api-key: TEST_API_KEY_123" \
  -d '{
    "tweet_data": "Hello from the corporate microblog!",
    "tweet_media_ids": []
  }'


Database migrations

Inside the web container:

flask db upgrade


Project structure

app/ – application package (models, API blueprints, auth helpers)

migrations/ – database migrations (Flask-Migrate)

Dockerfile, docker-compose.yml – container configuration

uploads/ – stored media files


Running with Docker

docker-compose up --build

The API will be available at: http://localhost:5000/api.


Endpoints (short overview)

POST /api/tweets

POST /api/medias

DELETE /api/tweets/<id>

POST /api/tweets/<id>/likes

DELETE /api/tweets/<id>/likes

POST /api/users/<id>/follow

DELETE /api/users/<id>/follow

GET /api/tweets

GET /api/users/me

GET /api/users/<id>


For error responses the format is:

{
  "result": false,
  "error_type": "str",
  "error_message": "str"
}


Further work

add Swagger/OpenAPI documentation for all endpoints;

add unit tests and coverage;

add linters and mypy configuration.
