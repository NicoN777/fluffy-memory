from rmq.rabbit import connection, LazyChannel
from rmq.conf import *
from rmq.utils import from_obj

sender = LazyChannel(connection=connection, type=direct_type, exchange=direct_exchange, durable=direct_durable,
                     queue=direct_queues)
with sender as s:
    for i in range(10):
        payload = from_obj({'id': 1, 'name': 'Toasty', 'age': 10, 'sleepers': 12})
        print(f'Message to be sent: {payload}')
        s.basic_publish(exchange=sender.exchange, routing_key=sender.routing_key, body=payload)
        print(f'Message sent!')