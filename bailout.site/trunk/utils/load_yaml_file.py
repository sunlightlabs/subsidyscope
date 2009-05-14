import yaml
from utils.logger import Logger

def load_yaml_file(filename, log=Logger()):
    log.info("Loading %s" % filename, 1)
    f = open(filename, mode='r')
    contents = f.read()
    f.close()
    return yaml.load(contents)

