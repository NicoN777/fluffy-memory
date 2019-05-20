from rabbit import connection, LazyRMQ
from conf import *

def initialize_rmq():
    """Initialize queues for direct and fanout examples"""
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
    initialize_rmq()

    print('Done')