import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

path = cfg['path']
programs = cfg['programs']

