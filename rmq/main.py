import argparse
from consumer import direct_receive, fanout_receive, topic_receive
from producer import direct_send, fanout_send, topic_send
from conf import *

def initialize_rmq():
    """Initialize queues for direct and fanout examples"""
    from rabbit import connection, LazyRMQ

    direct = LazyRMQ(connection=connection,
                            type=direct_type,
                            exchange=direct_exchange,
                            durable=direct_durable,
                            queues=direct_queues)

    fanout = LazyRMQ(
        connection=connection,
        type=fanout_type,
        exchange=fanout_exchange,
        durable=fanout_durable,
        queues=fanout_queues
    )

    topic = LazyRMQ(
        connection=connection,
        type=topic_type,
        exchange=topic_exchange,
        durable=topic_durable,
        queues=topic_queues,
        routing_keys=topic_routing_keys
    )

    direct.set_up()
    fanout.set_up()
    topic.set_up()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', help='Initializes DIRECT and FANOUT exchanges '
                                        'and queue bindings', action='store_true')

    parser.add_argument('--list-properties', help='See properties for examples', action='store_true')

    subparsers = parser.add_subparsers(dest='command')

    direct = subparsers.add_parser('direct')
    direct.add_argument('action', choices=['produce', 'consume'])

    fanout = subparsers.add_parser('fanout')
    fanout.add_argument('action', choices=['produce', 'consume'])
    fanout.add_argument('--queue-name', help='select a queue name to consume from, default fanout_1', default='fanout_1')

    topic = subparsers.add_parser('topic')
    topic.add_argument('action', choices=['produce', 'consume'])
    topic.add_argument('--routing-key', help='route a message with a key, default blue', default='blue')
    topic.add_argument('--queue-name', help='select a queue name to consume from, default blue_queue', default='blue_queue')

    args = parser.parse_args()
    if args.setup:
        print('Initializing RMQ')
        initialize_rmq()

    if args.list_properties:
        list_properties()

    if args.command == 'direct':
        if args.action == 'produce':
            print('Sending messages to the exchange')
            direct_send()
        else:
            direct_receive()
    elif args.command == 'fanout':
        print('Sending messages to the exchange')
        if args.action == 'produce':
            fanout_send()
        else:
            fanout_receive(args.queue_name)
    elif args.command == 'topic':
        print('Sending messages to the exchange')
        if args.action == 'produce':
            topic_send(args.routing_key)
        else:
            topic_receive(args.queue_name)
