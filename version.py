import toml
from typing import Literal

# Load a TOML file
# with open('config.toml', 'r') as f:
# 	config = toml.load(f)

# config['database']['level2'] = 'new added information'
# with open('config.toml', 'w') as f:
# 	toml.dump(config, f)

def get_config(path):
	with open(path, 'r') as f:
		config = toml.load(f)
	return config


def get_version(path:str):
	config = get_config(path)

	project_name = config['project']['name']
	version = config['project']['version']

	return {'project_name': project_name, 'version': version}

def increment_version(version:str, location: Literal['major','minor','patch'] = 'patch', increment=1):
	version = version.split('.')
	location = 0 if location == 'major' else 1 if location == 'minor' else 2
	version[location] = str(int(version[location]) + increment)
	return '.'.join(version)

def set_version(path:str):
	
	version = get_version(path)

	config = get_config(path)
	config['project']['version'] = increment_version()

	# with open('config.toml', 'w') as f:
    # 	toml.dump(config, f)


def invoke():
	# find projects from folder structure - these are paths
	# filter selected projects - must be given by user - this is just a name
	# for each selected project (if there is a change)
		# increment versions
		# collect versions and project names
	# for each project
		# if there is a reference
		# update the version
	