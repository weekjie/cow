class Respority(object):
    def __init__(self, url, username = "python", password = "python", type=""):
        self.url = url
        self.username = username
        self.passowrd = password
        self.type = type

    def __init_res(self):
        pass

    def show(self):
        return {"type": self.type, "url": self.url, "username": self.username}

    def stop_res(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def get_content(self, path, num):
        pass

    def get_latest(self, path):
        pass

    def get_latest_log(self, path, limit=10):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_val:
            print(exc_tb)
            raise exc_type(exc_val)

    def __enter__(self):
        return self.connect()


import svn.remote

class SVNRespority(Respority):
    def __init__(self, url, username = "python", password = "python"):
        super(SVNRespority, self).__init__(url, username, password, "svn")
        self.__init_res()

    def __init_res(self):
        self.res = svn.remote.RemoteClient(self.url, self.username, self.passowrd)
        return self

    def get_content(self, path):
        return self.res.cat(path)

    def get_info(self, path):
        info = VersionInfo.INIT()
        rel_info = self.res.info(path)
        info.set_author(rel_info.get("commit_author"))
        info.set_revision(rel_info.get("commit_revision"))
        info.set_type(rel_info.get("entry_kind"))
        info_log, info_date = [ (l.msg, l.date) for l in self.res.log_default(rel_filepath=path) ][0]
        info.set_log(info_log)
        info.set_date(info_date)
        return info



class VersionInfo(object):
    def __index__(self, revision="", author="", type="", log=""):
        self.revision = revision
        self.author = author
        self.type = type

    @classmethod
    def INIT(cls):
        return VersionInfo()

    def set_revision(self, revision):
        self.revision = revision

    def get_revison(self):
        return self.revision

    def set_author(self, author):
        self.author = author

    def get_author(self):
        return self.author

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_log(self, log):
        self.log = log

    def get_log(self):
        return  self.log

    def set_date(self, date):
        self.date = date

    def get_date(self):
        return self.date



class ResporityManager(object):
    def __init__(self,resporities):
        self.original = resporities
        self.__init_resporities()

    def __init_resporities(self):
        type_dict={
            "svn": SVNRespority,
        }
        self.resporities = {}
        for k, v in self.original.items():
            res_type = type_dict.get(v.get("type"))
            url = v.get("url")
            username = v.get("username")
            password = v.get("password")
            self.resporities[k] =  res_type(url, username, password)

    MANAGER = None
    @classmethod
    def instance(cls, resporities):
        if not cls.MANAGER:
            cls.MANAGER = ResporityManager(resporities)
        return cls.MANAGER

    def show_resporities(self):
        re = {}
        for k, v in self.resporities.items():
            re.update({k: v.show()})
        return re

    def get_respority(self, res_name):
        respority = self.resporities.get(res_name)
        if not respority:
            raise Exception("There is no configed respority neamed %s" % res_name)
        return  respority