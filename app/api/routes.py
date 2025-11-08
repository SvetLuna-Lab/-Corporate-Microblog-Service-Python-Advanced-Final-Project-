# app/api/routes.py

from typing import Any

from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

from .. import db
from ..models import User, Tweet, Media, Like, Follow
from ..auth import require_user
from . import api_bp
from .errors import api_error


# 1. POST /api/tweets – создать твит
@api_bp.post("/tweets")
@require_user
def create_tweet(current_user: User) -> Any:
    data = request.get_json(force=True, silent=True) or {}
    content = data.get("tweet_data")
    media_ids = data.get("tweet_media_ids", [])

    if not content:
        api_error("validation_error", "tweet_data is required")

    tweet = Tweet(content=content, author=current_user)
    db.session.add(tweet)
    db.session.flush()  # чтобы появился tweet.id

    if media_ids:
        medias = Media.query.filter(Media.id.in_(media_ids)).all()
        for m in medias:
            m.tweet_id = tweet.id

    db.session.commit()

    return jsonify({"result": True, "tweet_id": tweet.id})


# 2. POST /api/medias – загрузка файлов формы
@api_bp.post("/medias")
@require_user
def upload_media(current_user: User) -> Any:
    if "file" not in request.files:
        api_error("validation_error", "file field is required")

    file = request.files["file"]
    if file.filename == "":
        api_error("validation_error", "empty filename")

    filename = secure_filename(file.filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, filename)
    file.save(path)

    media = Media(filename=filename)
    db.session.add(media)
    db.session.commit()

    return jsonify({"result": True, "media_id": media.id})


# 3. DELETE /api/tweets/<id> – удалить твит
@api_bp.delete("/tweets/<int:tweet_id>")
@require_user
def delete_tweet(current_user: User, tweet_id: int) -> Any:
    tweet = Tweet.query.get_or_404(tweet_id)
    if tweet.author_id != current_user.id:
        api_error("permission_denied", "Cannot delete another user's tweet", 403)

    db.session.delete(tweet)
    db.session.commit()
    return jsonify({"result": True})


# 4. POST /api/tweets/<id>/likes – поставить лайк
@api_bp.post("/tweets/<int:tweet_id>/likes")
@require_user
def like_tweet(current_user: User, tweet_id: int) -> Any:
    tweet = Tweet.query.get_or_404(tweet_id)

    existing = Like.query.filter_by(
        user_id=current_user.id, tweet_id=tweet.id
    ).first()
    if existing:
        return jsonify({"result": True})  # уже лайкнул

    like = Like(user_id=current_user.id, tweet_id=tweet.id)
    db.session.add(like)
    db.session.commit()
    return jsonify({"result": True})


# 5. DELETE /api/tweets/<id>/likes – убрать лайк
@api_bp.delete("/tweets/<int:tweet_id>/likes")
@require_user
def unlike_tweet(current_user: User, tweet_id: int) -> Any:
    tweet = Tweet.query.get_or_404(tweet_id)

    like = Like.query.filter_by(
        user_id=current_user.id, tweet_id=tweet.id
    ).first()
    if like:
        db.session.delete(like)
        db.session.commit()
    return jsonify({"result": True})


# 6. POST /api/users/<id>/follow – зафоловить
@api_bp.post("/users/<int:user_id>/follow")
@require_user
def follow_user(current_user: User, user_id: int) -> Any:
    if current_user.id == user_id:
        api_error("validation_error", "Cannot follow yourself")

    target = User.query.get_or_404(user_id)

    existing = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=target.id,
    ).first()
    if not existing:
        f = Follow(follower_id=current_user.id, followed_id=target.id)
        db.session.add(f)
        db.session.commit()

    return jsonify({"result": True})


# 7. DELETE /api/users/<id>/follow – отписаться
@api_bp.delete("/users/<int:user_id>/follow")
@require_user
def unfollow_user(current_user: User, user_id: int) -> Any:
    target = User.query.get_or_404(user_id)

    existing = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=target.id,
    ).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    return jsonify({"result": True})


# 8. GET /api/tweets – лента твитов
@api_bp.get("/tweets")
@require_user
def get_feed(current_user: User) -> Any:
    # пользователи, на которых подписан current_user
    following_ids = [
        f.followed_id for f in current_user.following.all()
    ]

    if not following_ids:
        tweets = []
    else:
        # сортировка по популярности (кол-во лайков) и по дате
        tweets = (
            Tweet.query.filter(Tweet.author_id.in_(following_ids))
            .outerjoin(Like)
            .group_by(Tweet.id)
            .order_by(db.func.count(Like.id).desc(), Tweet.created_at.desc())
            .all()
        )

    result = []
    for t in tweets:
        attachments = [
            f"/media/{m.filename}" for m in t.medias.all()
        ]
        likes = [
            {"user_id": l.user_id, "name": l.user.name}
            for l in t.likes.all()
        ]
        result.append(
            {
                "id": t.id,
                "content": t.content,
                "attachments": attachments,
                "author": {"id": t.author.id, "name": t.author.name},
                "likes": likes,
            }
        )

    return jsonify({"result": True, "tweets": result})


# 9. GET /api/users/me
@api_bp.get("/users/me")
@require_user
def get_me(current_user: User) -> Any:
    user = current_user
    return jsonify({"result": True, "user": _serialize_user(user)})


# 10. GET /api/users/<id>
@api_bp.get("/users/<int:user_id>")
def get_user_profile(user_id: int) -> Any:
    user = User.query.get_or_404(user_id)
    return jsonify({"result": True, "user": _serialize_user(user)})


def _serialize_user(user: User) -> dict[str, Any]:
    followers = [
        {"id": f.follower.id, "name": f.follower.name}
        for f in user.followers.all()
    ]
    following = [
        {"id": f.followed.id, "name": f.followed.name}
        for f in user.following.all()
    ]
    return {
        "id": user.id,
        "name": user.name,
        "followers": followers,
        "following": following,
    }
