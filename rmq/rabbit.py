import pika
import time
from conf import *
from utils import from_obj

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




class LazyRMQ:

    def __init__(self, connection=None, type='', exchange='', routing_key='', durable=True, queues=None, *args, **kwargs):
        self.connection = connection
        self.type = type
        self.exchange = exchange
        self.routing_key = routing_key
        self.durable = durable
        self.queues = queues
        self.queue = kwargs.get('queue', '')
        self.channels = []

    def set_up(self):
        channel = self.connection.channel()
        print(self)
        exchange_declare = channel.exchange_declare(exchange=self.exchange,
                                                    exchange_type=self.type,
                                                    durable=self.durable)
        queue_declares = dict()
        bind_oks = dict()
        if self.queues:
            for queue in self.queues:
                queue_declares[queue] = channel.queue_declare(queue=queue, durable=self.durable)
                bind_oks[queue] = channel.queue_bind(queue=queue, exchange=self.exchange, routing_key=self.routing_key)
        print(f'Exchange declare: {exchange_declare}\n'
              f'Queue declares: {queue_declares}\n'
              f'Bind oks: {bind_oks}')

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


if __name__ == '__main__':
    #Settings for direct
    # direct = RabbitAdmin(connection, exchange=direct_exchange, queue=direct_queue, durable=direct_durable)
    #Settings for fanout
    # fanout = RabbitAdmin(connection, exchange=fanout_exchange, durable=fanout_durable, kwargs={'queues': fanout_queues})

    fanout_sender = LazyRMQ(
        connection=connection,
        type=fanout_type,
        exchange=fanout_exchange,
        durable=fanout_durable,
        queues=fanout_queues
    )

    fanout_sender.set_up()


    print('')


