# consumer.py
# Consuming from queues bound to direct and fanout_exchanges

import argparse
from rabbit import connection, LazyRMQ
from conf import *
from utils import to_str, coroutine
import time
import random

@coroutine
def complete():
    while True:
        item = yield
        print(f'COMPLETE {item}')

def todo_callback(channel, method_frame, header_frame, body):
    todo = to_str(body)
    # Pretend theres some processing in the background...
    if not todo['completed']:
        random_sleep_time = random.randint(2,4)
        print(f'Todo {todo} is not complete... waiting for {random_sleep_time} seconds...')
        time.sleep(random_sleep_time)
        todo['completed'] = True
    complete().send(todo)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def notification_callback(channel, method_frame, header_frame, body):
    message = to_str(body)
    print(message)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def direct_receive():
    receiver = LazyRMQ(connection=connection,
                       **{'queue': 'direct_1'})
    with receiver as r:
        print(f'[Consumer] Waiting for messages from queue [{receiver.queue}]...')
        r.basic_qos(prefetch_count=1)
        r.basic_consume(queue=receiver.queue, on_message_callback=todo_callback)
        r.start_consuming()

def fanout_receive_1():
    fanout_receiver_1 = LazyRMQ(connection=connection,
                                exchange=fanout_exchange,
                                **{'queue': 'fanout_1'})
    with fanout_receiver_1 as r:
        print(f'Waiting for messages from: {fanout_receiver_1.queue}')
        r.basic_qos(prefetch_count=1)
        r.basic_consume(queue=fanout_receiver_1.queue, on_message_callback=notification_callback)
        r.start_consuming()

def fanout_receive_2():
    fanout_receiver_2 = LazyRMQ(connection=connection,
                                exchange=fanout_exchange,
                                **{'queue': 'fanout_2'})

    with fanout_receiver_2 as r:
        print(f'Waiting for messages from: {fanout_receiver_2.queue}')
        r.basic_qos(prefetch_count=1)
        r.basic_consume(queue=fanout_receiver_2.queue, on_message_callback=notification_callback)
        r.start_consuming()

