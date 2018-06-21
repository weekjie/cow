# -*- coding: utf-8 -*-

import time
from threading import Thread

from ._app_config import RESPORITY_MANAGER



#每个版本的数据模板类
#获取改版本的内容 / 提交者 / 日志
class Versioner(object):
	def __init__(self, respority, path):
		self.repority = respority
		self.path = path
		self.content = None
		self._init()

	def _init(self):
		self.res = RESPORITY_MANAGER.get_respority(self.repority)
		info = self.res.get_info(self.path)
		self.author = info.get_author()
		self.revision = info.get_revison()
		self.log = info.get_log()
		self.date = info.get_date()
		self.type = info.get_type()

	def get_content(self):
		if self.type == "file":
			self.content = self.res.get_content(self.path)
			return self.content
		else:
			raise Exception("The type of resource is not file.")


	def get_author(self):
		return self.author

	def get_log(self):
		return self.log

	def get_revision(self):
		return self.revision

	def get_date(self):
		return self.date

	def get_respority(self):
		return self.repority

	def get_path(self):
		return self.path

#缓存保存时间 , 秒为单位
CLEAN_TIME_OUT = 60 * 60 * 24

#缓存管理类 , 单类型
#获取所有的版本数据的入口类
#versions -- dict类型 , 根据id找到对应的缓存数据及保存时的时间戳 , 时间戳用于清理缓存 .
#latest_versions -- dict类型 , 缓存访问过的路径的最新版本号
class VersionManager(object):
	def __init__(self):
		self.versioners = {}

    #工厂方法
	MANAGER = None
	@classmethod
	def INIT(cls):
		if not cls.MANAGER:
			cls.MANAGER = VersionManager()
		return cls.MANAGER

    #根据路径和版本号获取对应的版本数据
    #版本号如何是None , 则认为是获取最新版本号
	def get_versioner(self, repority, path):
		return self._versioners_manager(repority, path, manager_type=1)[0]

    #根据路劲刷新缓存中的最新版本号和版本数据
    #并返回版本数据
	def flush_version(self, repority, path):
		return self._versioners_manager(repority, path, manager_type=2)[0]

    #管理数据缓存 , 三种管理方式
	#获取 : 1
	#刷新获取 : 2
	#删除 : 3
	def _versioners_manager(self, respority, path, id = "",  manager_type = 1):
		if not id:
			id = respority + ":" + path

		def _get(inner_cache, iid):
			if not inner_cache.get(iid):
				inner_cache[iid] = (Versioner(*iid.split(":")), time.time())
			return inner_cache.get(iid)

		def _flush_get(inner_cache, iid):
			inner_cache[iid] = (Versioner(*iid.split(":")), time.time())
			return inner_cache.get(iid)

		def _del(inner_cache, iid):
			now = time.time()
			itime =  inner_cache.get(iid)[1]
			if now -  itime > CLEAN_TIME_OUT:
				tmp = inner_cache.pop(iid)

		if manager_type == 1:
			return _get(self.versioners, id)
		elif manager_type == 2:
			return  _flush_get(self.versioners, id)
		elif manager_type == 3:
			return _del(self.versioners, id)
		else:
			pass

    #清理缓存数据用
	def clean(self):
		for id in self.versioners.keys():
			self._versioners_manager("", "", id=id, manager_type=3)

#清理缓存的线程
class Cleaner(Thread):
	def __init__(self):
		super(Cleaner, self).__init__()
		self.manager = VersionManager.INIT()

	def run(self):
		while True:
			self.manager.clean()
			time.sleep(5)

#清理缓存的方法
def __run_cleaner():
	cleaner = Cleaner()
	cleaner.start()

#启动清理缓存
__run_cleaner()

VERSION_MANAGER = VersionManager.INIT()
