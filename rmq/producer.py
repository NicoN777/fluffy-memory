from rabbit import connection, LazyChannel
from conf import *
from utils import from_obj
from requester import request_todos


sender = LazyChannel(connection=connection,
                     type=direct_type,
                     exchange=direct_exchange,
                     durable=direct_durable,
                     queue=direct_queue)

def direct_send():
    with sender as s:
        for todo in request_todos():
            payload = todo
            print(f'Message to be sent: {payload}')
            s.basic_publish(exchange=sender.exchange, routing_key=sender.routing_key, body=from_obj(payload))
            print(f'Message sent!')

if __name__ == '__main__':
    direct_send()