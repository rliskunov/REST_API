from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from videoblog.base_view import BaseView

from videoblog import logger, docs
from videoblog.models import Video
from videoblog.schemas import VideoSchema

videos = Blueprint("videos", __name__)


class ListView(BaseView):
    @marshal_with(VideoSchema(many=True))
    def get(self):
        try:
            videos = Video.get_list()
        except Exception as e:
            logger.warning(f"tutorials - read action failed with errors: {e}")
            return {"message": str(e)}, 400
        return videos


@videos.route("/tutorials", methods=["GET"])
@jwt_required()
@marshal_with(VideoSchema(many=True))
def get_list():
    user_id: str = ""
    try:
        user_id = get_jwt_identity()
        videos: list = Video.get_user_list(user_id=user_id)
    except Exception as e:
        logger.warning(f"user: {user_id} tutorials - read action failed with errors: {e}")
        return {"message": str(e)}, 400
    return videos


@videos.route("/tutorials", methods=["POST"])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def add_list(**kwargs):
    user_id: str = ""
    try:
        user_id = get_jwt_identity()
        video: Video = Video(
            user_id=user_id,
            **kwargs
        )
        video.save()
    except Exception as e:
        logger.warning(f"user: {user_id} tutorials - create action failed with errors: {e}")
        return {"message": str(e)}, 400
    return video


@videos.route("/tutorials/<int:tutorials_id>", methods=["PUT"])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(tutorials_id, **kwargs):
    user_id: str = ""
    try:
        user_id = get_jwt_identity()
        video: Video = Video.get(tutorials_id, user_id)
        video.update(**kwargs)
    except Exception as e:
        logger.warning(f"user: {user_id} tutorial: {tutorials_id} - update action failed with errors: {e}")
        return {"message": str(e)}, 400
    return video


@videos.route("/tutorials/<int:tutorials_id>", methods=["DELETE"])
@jwt_required()
@marshal_with(VideoSchema)
def delete_list(tutorials_id):
    user_id: str = ""
    try:
        user_id = get_jwt_identity()
        video: Video = Video.get(tutorials_id, user_id)
        video.delete()
    except Exception as e:
        logger.warning(f"user: {user_id} tutorial: {tutorials_id} - delete action failed with errors: {e}")
        return {"message": str(e)}, 400
    return '', 204


@videos.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ["Invalid request"])
    logger.warning(f"Invalid input params: {messages}")
    if headers:
        return jsonify({"messages": messages}), 400, headers
    else:
        return jsonify({"messages": messages}), 400


docs.register(get_list, blueprint="videos")
docs.register(add_list, blueprint="videos")
docs.register(update_list, blueprint="videos")
docs.register(delete_list, blueprint="videos")
ListView.register(videos, docs, '/main', 'listview')