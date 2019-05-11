from rmq.rabbit import connection, LazyChannel
from rmq.conf import *
from rmq.utils import from_str
import time

def callback(channel, method_frame, header_frame, body):
    message = from_str(body)
    print(message)
    time.sleep(5)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


receiver = LazyChannel(connection=connection,
                       type=direct_type,
                       exchange=direct_exchange,
                       durable=direct_durable,
                       queue=direct_queues)

with receiver as r:
    print(f'[Consumer] Waiting for messages from queue [{receiver.queue}]...')
    r.basic_qos(prefetch_count=1)
    r.basic_consume(queue=receiver.queue, on_message_callback=callback)
    r.start_consuming()



