from .conf import *
from .rabbit import connection, LazyChannel
from .utils import *

broadcaster = LazyChannel(connection=connection, type=fanout_type, exchange=fanout_exchange, durable=fanout_durable)

with broadcaster as bcast:
    payload = from_obj({'test': 182, 'session_id': 100})
    bcast.basic_publish(exchange=fanout_exchange, routing_key=broadcaster.routing_key, body=payload)