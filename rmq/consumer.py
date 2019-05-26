# consumer.py
# Consuming from queues bound to direct and fanout_exchanges

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

def direct_callback(channel, method_frame, header_frame, body):
    todo = to_str(body)
    # Pretend theres some processing in the background...
    # Once its complete send to complete coroutine for
    if not todo['completed']:
        random_sleep_time = random.randint(2,4)
        print(f"Todo with id: {todo['id']} by User: {todo['userId']} is not complete... waiting for {random_sleep_time} seconds...")
        time.sleep(random_sleep_time)
        todo['completed'] = True
    complete().send(todo)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def fanout_callback(channel, method_frame, header_frame, body):
    message = to_str(body)
    print(message)
    time.sleep(random.randint(2,7))
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def topic_callback(channel, method_frame, header_frame, body):
    # message = to_str(body)
    message = body
    print(message)
    time.sleep(random.randint(2,7))
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def receive(receiver, callback):
    with receiver as r:
        print(f'[Consumer] Waiting for messages from queue [{receiver.queue}]...')
        r.basic_qos(prefetch_count=1)
        r.basic_consume(queue=receiver.queue, on_message_callback=callback)
        r.start_consuming()

def direct_receive():
    direct_receiver = LazyRMQ(connection=connection,
                       **{'queue': 'direct_1'})
    receive(direct_receiver, direct_callback)

def topic_receive(queue_name):
    topic_receiver = LazyRMQ(connection=connection,
                             exchange=topic_exchange,
                             **{'queue': f'{queue_name}'})
    receive(topic_receiver, topic_callback)

def fanout_receive(queue_name):
    fanout_receiver = LazyRMQ(connection=connection,
                                exchange=fanout_exchange,
                                **{'queue': f'{queue_name}'})
    receive(fanout_receiver, fanout_callback)


