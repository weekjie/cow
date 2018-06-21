from os import path
import yaml

from respority_manager import ResporityManager
import src_app.config as CONFIG

print(path.abspath("."))

def parse():
	with open(path.abspath(".") + "/" + CONFIG.RES_CONFIG) as f:
		data = yaml.load(f).get("repositories")
	return data

RESPORITY_MANAGER = ResporityManager.instance(parse())



