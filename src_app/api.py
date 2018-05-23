from flask import Blueprint, json

from version_manager import repositories

api = Blueprint("api", __name__)

@api.route("/")
def index():
    return json.jsonify(repositories)