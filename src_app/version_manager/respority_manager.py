class Respority(object):
    def __init__(self, url, username = "python", password = "python", type=""):
        self.useranem = username
        self.passowrd = password
        self.type = type

    def __init_res(self):
        pass

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
        self.init_res()

    def __init_res(self):
        self.res = svn.remote.RemoteClient(self.url, self.username, self.passowrd)
        return self

    def get_content(self, path, num):
        return self.res.cat(path, num)

    def get_latest(self, path):
        return int(self.res.info(path).get("entry_revision"))

    def get_latest_log(self, path, limit=10):
        p =  self.res.log_default(rel_filepath=path, limit=limit)
        try:
            log_arr = [VersionLog(log.revision, log.author, log.msg) for log in p]
            return log_arr
        except Exception,e:
            raise Exception(e)

class VersionLog(object):
    def __index__(self, version_num, author, msg):
        self.version_num = version_num
        self.author = author
        self.msg = msg

    def get_version_num(self):
        return self.version_num

    def get_author(self):
        return self.author

    def get_msg(self):
        return self.msg

class ResporityManager(object):
    def __init__(self):
        resporities = {}

    MANAGER = None
    @classmethod
    def instance(cls):
        if not cls.MANAGER:
            cls.MANAGER = ResporityManager()
        return cls.MANAGER



    def get_respority(self):
        pass