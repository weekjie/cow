from flask import Blueprint, json, abort

from src_app.version_manager import RESPORITY_MANAGER, VERSION_MANAGER
from src_app.service import create_service

api = Blueprint("api", __name__)

def _get_versioner(resource_name):
    resource_data = create_service().get_servcies().get(resource_name)
    if not resource_data:
        print "There is no resourc named %s" % resource_name
        abort(404)
    respority = resource_data.get("respority")
    path = resource_data.get("path")
    return  VERSION_MANAGER.get_versioner(respority, path)

@api.route("/resporities")
def resporities():
    return json.jsonify(RESPORITY_MANAGER.show_resporities())

@api.route("/services")
def servcies():
    return json.jsonify(create_service().get_servcies())

@api.route('/info/<resource_name>')
def info(resource_name):
    versioner =  _get_versioner(resource_name)
    result = {"commit_author": versioner.get_author(), "commit_log": versioner.get_log(), \
              "revision": versioner.get_revision(), "commit_date": versioner.get_date()}
    return json.jsonify(result)

@api.route("/content/<resource_name>")
def cat(resource_name):
    versioner =  _get_versioner(resource_name)
    result = {"respority": versioner.get_respority(), "path": versioner.get_path(), \
              "content": versioner.get_content()}
    return json.jsonify(result)