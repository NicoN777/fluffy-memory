from rmq.rabbit import connection, LazyChannel
from rmq.conf import *
from rmq.utils import from_str
import time

def callback(channel, method_frame, header_frame, body):
    # print('Channel: ', channel)
    # print('Method Frame: ', method_frame)
    # print('Header Frame: ', header_frame)
    # print('Body: ', body)
    message = from_str(body)
    print(message)
    print(type(message))
    for name, value in message.items():
        print(name, value)

    time.sleep(12)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


receiver = LazyChannel(connection=connection,
                       type=direct_type,
                       exchange=direct_exchange,
                       durable=direct_durable,
                       queue=direct_queues)

with receiver as r:
    print(f'[Consumer] Waiting for messages from queue [{receiver.queue}]...')
    r.basic_consume(queue=receiver.queue, on_message_callback=callback)
    r.start_consuming()



