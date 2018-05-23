from flask import Flask
from .api import api
from .version_manager import VersionManager

def create_app():
    app = Flask(__name__)
    app.config.from_object("src_app.config")
    app.register_blueprint(api, url_prefix="/api")
    return app
