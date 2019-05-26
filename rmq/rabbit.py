import pika
import time
from conf import *
from collections import defaultdict
from itertools import zip_longest

pika_credentials = pika.PlainCredentials(username=user, password=password)
connection_params = pika.ConnectionParameters(host=host, port=port, credentials=pika_credentials)
connection = pika.BlockingConnection(parameters=connection_params)


class RabbitAdmin:
    """RMQ "Admin" for monitoring"""

    def __init__(self, connection, exchange, queue, durable, *args, **kwargs):
        self.__admin_channel = connection.channel()
        self.__exchange = exchange
        self.__queue = queue
        self.__durable = durable

        if kwargs:
            self.queues = kwargs.pop('queues')

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

    def monitor(self):
        print(f'Queue Name: {self.queue_name}')
        while self.consumer_count != 0 and self.message_count !=0:
            print(f'Consumer count: {self.consumer_count}\n'
                  f'Message count: {self.message_count}')
            time.sleep(2)

    def purge(self):
        messages_deleted = self.__admin_channel.queue_purge(queue=self.__queue)
        print(f'{messages_deleted} messages deleted from queue[{self.__queue}]')

    def delete(self):
        self.admin_channel.que_delete(queue=self.queue)

    def delete_queues(self):
        if self.queues:
            for queue in self.queues:
                self.admin_channel.queue_delete(queue=queue)


    def set_up(self):
        binds = {}
        self.exchange_declare = self.admin_channel.exchange_declare(exchange=self.__exchange,
                                                                      exchange_type=self._type,
                                                                      durable=self.durable)
        for queue in self.queues:
            bind_ok = self.admin_channel.queue_bind(queue=queue,
                                                    exchange=self.__exchange,
                                                    durable=self.__durable)
            binds[queue] = bind_ok
        return binds

class LazyRMQ:

    def __init__(self, connection=None, type='', exchange='', routing_keys=list(), durable=True, queues=None, *args, **kwargs):
        self.connection = connection
        self.type = type
        self.exchange = exchange
        self.routing_keys = routing_keys
        self.durable = durable
        self.queues = queues
        self.queue = kwargs.get('queue') or  ''
        self.routing_key = kwargs.get('routing_key') or ''
        self.channels = []

    def set_up(self):
        channel = self.connection.channel()
        print(self)
        exchange_declare = channel.exchange_declare(exchange=self.exchange,
                                                    exchange_type=self.type,
                                                    durable=self.durable)
        queue_declares = dict()
        bind_oks = defaultdict(list)

        print(f'Exchange declare: {exchange_declare}')

        for queue, _ in zip_longest(self.queues, self.routing_keys, fillvalue=''):
            queue_declares[queue] = channel.queue_declare(queue=queue, durable=self.durable)
            print(f'Queue: {queue}')
            _ = _.split('-')
            for routing_key in _:
                print(f'bound to --> {routing_key}')
                bind_oks[queue].append(channel.queue_bind(queue=queue, exchange=self.exchange, routing_key=routing_key))

    def __enter__(self):
        channel = self.connection.channel()
        self.channels.append(channel)
        print(f'Channels open: {len(self.channels)}')
        return channel

    def __exit__(self, ty, val, tb):
        self.channels.pop().close()
        print(f'Channel closed.')

    def __str__(self):
        return f'Type: {self.type}\n' \
               f'Exchange: {self.exchange}\n' \
               f'Routing Key: {self.routing_key}\n' \
               f'Durable: {self.durable}\n' \
               f'Queues={self.queues}\n' \
               f'Read from queue: {self.queue}'
