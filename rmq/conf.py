# conf.py
# Read configurations from properties file.

import configparser
import os

secret_path = os.environ.get('RMQ_PATH')
secret_file = os.path.join(secret_path, 'rmq.ini')
config = configparser.RawConfigParser()

print(f'Loading from: {secret_file}')
config.read(secret_file)

#General
user = config.get('General', 'user')
password = config.get('General', 'password')
host = config.get('General', 'host')
port = config.get('General', 'port')
uri = config.get('General', 'uri')

#Direct
direct_type = 'direct'
direct_exchange = config.get('Direct', 'exchange')
direct_durable = config.getboolean('Direct', 'durable')
direct_queues = config.get('Direct', 'queues').split()

#Fanout
fanout_type = 'fanout'
fanout_exchange = config.get('Fanout', 'exchange')
fanout_durable = config.get('Fanout', 'durable')
fanout_queues = config.get('Fanout', 'queues').split()

#Routing

#Header


if __name__ == '__main__':
    for section in config.sections():
        print(f'-- Section: {section} --')
        for option in config.options(section):
            print (f'{option}= {config.get(section, option)}')
