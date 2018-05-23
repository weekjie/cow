import time
from threading import Thread

from .utile import get_latest, get_resource

class Versioner(object):
	def __init__(self, id="", path="", num=""):
		if not id:
			self.path, self.num = id.split(":")
		self.__get_resource()

	def __get_resource(self):
		self.author, self.content, self.log = get_resource(self.path, self.num)

	def rollback(self):
		pass

	def get_content(self):
		return self.content


	def get_author(self):
		return self.author

	def get_log(self):
		return self.log

CLEAN_TIME_OUT = 60 * 60 * 24

class VersionManager(object):
	def __init__(self):
		self.versioners = {}
		self.latest_versions = {}

	MANAGER = None
	@classmethod
	def instance(cls):
		if not cls.MANAGER:
			cls.MANAGER = VersionManager()
		return cls.MANAGER

	def __get_latest_num(self, path):
		if not self.latest_versions.has_key(path):
			self.latest_versions[path] = get_latest(path)
		return self.latest_versions[path]


	def __get_id(self, path, num = None):
		if not num:
			num = self.__get_latest_num(path)
		return path + ":" + num


	def get_versioner(self, path, num = None):
		id = self.__get_id(path, num)
		return self.__get_versioner(id)


	def flush_version(self, path):
		self.latest_versions.pop(path)
		id = self.__get_id(path, None)
		self.__clean_version(id)
		return self.__get_versioner(id)

	def __get_versioner(self, id):
		if not self.versioners.has_key(id):
			self.versioners[id] = (Versioner(id=id), time.time())
		return self.versioners[id]

	def __clean_version(self, id):
		if self.versioners.has_key(id):
			self.versioners.pop(id)

	def clean(self):
		now = time.time()
		for id, version_tpule in self.versioners.items():
			if now - version_tpule[1] > CLEAN_TIME_OUT :
				self.__clean_version(id)


class Cleaner(Thread):
	def __init__(self):
		super(Cleaner, self).__init__()
		self.manager = VersionManager.instance()

	def run(self):
		while True:
			self.manager.clean()
			time.sleep(5)

def __run_cleaner():
	cleaner = Cleaner()
	cleaner.start()

__run_cleaner()
