# conf.py
# Read _configurations from properties file.

import configparser
import os
import logging

_secret_path = os.environ.get('RMQ_PATH')
_secret_file = os.path.join(_secret_path, 'rmq.ini')
_config = configparser.ConfigParser()
_config.read(_secret_file)

def get_pika_params(section:str):
    params = get_properties(section)
    if 'queues' in params.keys():
        params['queues'] = params.get('queues', '').split()
    if 'routing_keys' in params.keys():
        params['routing_keys'] = params.get('routing_keys', '').split()
    return params

def get_properties(section:str):
    if section in _config.sections():
        properties = dict(_config[section])
    else:
        raise ValueError(f'Section: {section}, not in properties')
    return properties

def list_properties():
    all_properties = {section:{option:value for (option, value) in _config[section].items()} for section in  _config.sections()}
    for section, _ in all_properties.items():
        print(f'--- Section: {section} ---')
        for _ in _.items():
            print(_)

#Connection
user = _config.get('General', 'user')
password = _config.get('General', 'password')
host = _config.get('General', 'host')
port = _config.get('General', 'port')
uri = _config.get('General', 'uri')

#Direct
direct_type = _config.get('Direct', 'type')
direct_exchange = _config.get('Direct', 'exchange')
direct_durable = _config.getboolean('Direct', 'durable')
direct_queues = _config.get('Direct', 'queues').split()

#Fanout
fanout_type = _config.get('Fanout', 'type')
fanout_exchange = _config.get('Fanout', 'exchange')
fanout_durable = _config.get('Fanout', 'durable')
fanout_queues = _config.get('Fanout', 'queues').split()

#Topic
topic_type = _config.get('Topic', 'type')
topic = _config._sections['Topic']
topic_exchange = _config.get('Topic', 'exchange')
topic_durable = _config.getboolean('Topic', 'durable')
topic_queues = _config.get('Topic', 'queues').split()
topic_routing_keys = _config.get('Topic', 'routing_keys').split()

#Header

