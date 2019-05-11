import pika

from rmq.conf import *
from rmq.utils import from_obj

pika_credentials = pika.PlainCredentials(username=user, password=password)
connection_params = pika.ConnectionParameters(host=host, port=port, credentials=pika_credentials)
connection = pika.BlockingConnection(parameters=connection_params)


class RabbitAdmin:

    def __init__(self, connection, exchange, queue, durable):
        self.__admin_channel = connection.channel()
        self.__exchange = exchange
        self.__queue = queue
        self.__durable = durable

    def __declare_ok(self):
        return self.__admin_channel.queue_declare(queue=self.__queue, durable=self.__durable)

    @property
    def admin_channel(self):
        return self.__admin_channel

    @property
    def queue_name(self):
        return self.__queue

    @property
    def message_count(self):
        return self.__declare_ok().method.message_count

    @property
    def consumer_count(self):
        return self.__declare_ok().method.consumer_count

    def purge(self):
        messages_deleted = self.__admin_channel.purge_ok(queue=self.__queue, durable=self.__durable)
        print(f'{messages_deleted} messages deleted from queue[{self.__queue}]')


class LazyChannel:

    def __init__(self, connection=None, type='', exchange='', routing_key='', durable=True, queue=''):
        self.connection = connection
        self.type = type
        self.exchange = exchange
        self.routing_key = routing_key
        self.durable = durable
        self.queue = queue
        self.channels = []

    def __enter__(self):
        channel = self.connection.channel()
        exchange_declare = channel.exchange_declare(exchange=self.exchange,
                                                    exchange_type=self.type,
                                                    durable=self.durable)
        queue_declare = channel.queue_declare(queue=self.queue, durable=self.durable)
        bind_ok = channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=self.routing_key)
        print(exchange_declare, queue_declare, bind_ok)
        self.channels.append(channel)
        print(f'Channels open: {len(self.channels)}')
        return channel

    def __exit__(self, ty, val, tb):
        self.channels.pop().close()
        print(f'Channel closed.')


if __name__ == '__main__':
    rmq_admin = RabbitAdmin(connection, direct_exchange, direct_queues, direct_durable)
    print(rmq_admin.queue_name)





