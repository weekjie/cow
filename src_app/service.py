from os import path

import yaml

import src_app.config as CONFIG

class SrcAppServices(object):
    SRCAPPSERVICES = None
    SERVICES_DICT = path.abspath(".") + "/" + CONFIG.SERVICES_DICT

    def __init__(self):
        self._init_service()

    @classmethod
    def INIT(cls):
        if not SrcAppServices.SRCAPPSERVICES:
            SrcAppServices.SRCAPPSERVICES = SrcAppServices()
        return  SrcAppServices.SRCAPPSERVICES

    def _init_service(self):
        with open(SrcAppServices.SERVICES_DICT) as f:
            self.services_data = yaml.load(f).get("services")

    def get_servcies(self):
        return self.services_data

def create_service():
    return SrcAppServices.INIT()


