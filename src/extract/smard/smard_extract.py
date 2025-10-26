from pprint import pprint
import yaml 

config_path_yaml = '../config/project.yaml'

with open(config_path_yaml, 'r') as file:
    cnf = yaml.safe_load(file)

pprint(cnf['sources']['smard'])
