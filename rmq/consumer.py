from rabbit import connection, LazyChannel
from conf import *
from utils import to_str, coroutine
import time
import random


receiver = LazyChannel(connection=connection,
                       type=direct_type,
                       exchange=direct_exchange,
                       durable=direct_durable,
                       queue=direct_queue)

@coroutine
def complete():
    while True:
        item = yield
        print(f'COMPLETE {item}')

def todo_callback(channel, method_frame, header_frame, body):
    todo = to_str(body)
    if not todo['completed']:
        random_sleep_time = random.randint(5,10)
        print(f'Todo {todo} is not complete... waiting for {random_sleep_time} seconds...')
        time.sleep(random_sleep_time)
        todo['completed'] = True
    complete().send(todo)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def direct_receive():
    with receiver as r:
        print(f'[Consumer] Waiting for messages from queue [{receiver.queue}]...')
        r.basic_qos(prefetch_count=1)
        r.basic_consume(queue=receiver.queue, on_message_callback=todo_callback)
        r.start_consuming()


if __name__== '__main__':
    direct_receive()



