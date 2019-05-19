import pika
import time
from conf import *

pika_credentials = pika.PlainCredentials(username=user, password=password)
connection_params = pika.ConnectionParameters(host=host, port=port, credentials=pika_credentials)
connection = pika.BlockingConnection(parameters=connection_params)


class RabbitAdmin:

    def __init__(self, connection, exchange, queue, durable, *args, **kwargs):
        self.__admin_channel = connection.channel()
        self.__exchange = exchange
        self.__queue = queue
        self.__durable = durable

    def __declare_ok(self):
        return self.__admin_channel.queue_declare(queue=self.__queue, durable=self.__durable)


    # def _refresh(self):
    #     if self.admin_channel.is_closed or self.admin_channel.is_closing:
    #         self.co
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
        self.channels.append(channel)
        print(f'Channels open: {len(self.channels)}')
        return channel

    def __exit__(self, ty, val, tb):
        self.channels.pop().close()
        print(f'Channel closed.')



if __name__ == '__main__':
    #Settings for direct
    direct = RabbitAdmin(connection, exchange=direct_exchange, queue=direct_queue, durable=direct_durable)
    #Settings for fanout
    # fanout = RabbitAdmin(connection, exchange=fanout_exchange, durable=fanout_durable, kwargs={'queues': fanout_queues})
    print('')


