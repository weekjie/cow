from flask import Flask
from .api import api
from service import create_service

def create_app():
    app = Flask(__name__)
    create_service()
    app.config.from_object("src_app.config")
    app.register_blueprint(api, url_prefix="/api")
    return app
