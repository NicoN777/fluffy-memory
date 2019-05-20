import argparse
from consumer import (direct_receive, fanout_receive_1, fanout_receive_2)
from producer import direct_send, fanout_send
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

    direct.set_up()
    fanout.set_up()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', help='Initializes DIRECT and FANOUT exchanges '
                                        'and queue bindings', action='store_true')


    parser.add_argument('type', help='direct or fanout', choices=['direct', 'fanout'])
    #subparsers are inviked based on the value of the first positiional argument




    parser.add_argument('action', help='produce items or consue itms', choices=['produce', 'consume'])

    args = parser.parse_args()
    if args.setup:
        print('Initializing RMQ')
        initialize_rmq()

    if args.type == 'direct':
        if args.action == 'produce':
            print('Sending messages to the exchange')
            direct_send()
        else:
            direct_receive()
    else:
        if args.action == 'produce':
            fanout_send()
        else:
            fanout_receive_1()

