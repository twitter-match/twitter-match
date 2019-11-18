import os
import yaml

yaml_path = os.path.join(
    os.path.dirname(__file__), 'consts.yml')
with open(yaml_path, 'r') as f:
    APIS_CONSTS = yaml.load(f, Loader=yaml.FullLoader)