# producer.py
# Produce "" data and push to exchanges

from rabbit import connection, LazyRMQ
from conf import *
from utils import from_obj
from requester import request_todos, request_comments

def direct_send():
    direct_sender = LazyRMQ(connection=connection, exchange=direct_exchange)
    with direct_sender as s:
        for todo in request_todos():
            payload = todo
            print(f'Message to be sent: {payload}')
            s.basic_publish(exchange=direct_sender.exchange, routing_key=direct_sender.routing_key, body=from_obj(payload))
            print(f'Message sent!')
            
def fanout_send():
    fanout_sender = LazyRMQ(connection=connection, exchange=fanout_exchange)
    with fanout_sender as s:
        for post in request_comments():
            payload = post
            print(f'Message to be sent: {payload}')
            s.basic_publish(exchange=fanout_sender.exchange, routing_key=fanout_sender.routing_key, body=from_obj(payload))

def topic_send():
    topic_sender = LazyRMQ(connection=connection, exchange=topic_exchange)
    pass

if __name__ == '__main__':
    direct_send()
    fanout_send()