
from ._app_config import repositories

def verify_path_format(func):
	def wrapper(*args, **kwargs):
		path = args[0]
		if len(path.split('/')) != 3:
			raise Exception("Wrong repository path, it's should be like '${project]/${module}/${file}'.")
		return func(*args, **kwargs)
	return wrapper

@verify_path_format
def get_latest(path):
	url = ""
	pass

@verify_path_format
def get_resource(path, num):

	content = ""
	log = ""
	author = ""
	return  author, content, log


def _get_url(path):
	project, module, file_name = path.split('/')
	url = repositories.get(project)
	if not url:
		raise Exception("There is no conifg aboout project -- %s" % project)
	url = url.rstrip("/")
	res_type = url[url.rfind("/") + 1:]
	return url, res_type
