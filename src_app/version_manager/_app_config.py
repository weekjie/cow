from os import path
import yaml

print(path.abspath("."))

repositories = {}
with open(path.abspath(".") + "/src_app/res.yml") as f:
	data = yaml.load(f)[0].get("repositories")
	for inner_dict in data:
		repositories.update(inner_dict)

