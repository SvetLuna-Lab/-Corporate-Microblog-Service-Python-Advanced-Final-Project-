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

The project uses:

- **Flask** as the web framework,
- **PostgreSQL** as the database,
- **SQLAlchemy + Flask-Migrate** for ORM and migrations,
- **Docker + docker-compose** for local development and deployment.

The code is structured as a small production-style service: blueprints for the API, separate models and auth helpers, unified error format, and a docker-compose configuration to run the app together with PostgreSQL.


Backend for a corporate microblogging service (Twitter-like), implemented with Flask and PostgreSQL.

The service supports:

- creating and deleting tweets (with optional media);
- liking and unliking tweets;
- following and unfollowing users;
- fetching a feed of tweets from followed users, sorted by popularity;
- fetching user profiles (`/users/me` and `/users/<id>`).

All endpoints use `api-key` HTTP header to identify the current user.

## Tech stack

- Python, Flask
- PostgreSQL
- SQLAlchemy, Flask-Migrate
- Docker, docker-compose

## Running with Docker

```bash
docker-compose up --build


The API will be available at: http://localhost:5000/api



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

Further work:

add Swagger/OpenAPI documentation for all endpoints;

add unit tests and coverage;

add linters and mypy configuration.
