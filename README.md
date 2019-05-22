# fluffy-memory
RabbitMQ Examples
Make sure docker is installed then run this command:

```commandline 
docker run -d --hostname bunny --name b-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```

The main entry point to load parameters for RabbitMQ configs is:
```commandline
python rmq/main.py --setup
```

See what has been loaded and set up

```commandline
python rmq/main.py --list-properties
```

### Direct Exchange Example:
##### Send messages to queue bound to a direct exchange:
```commandline
python rmq/main.py direct produce
```

##### Consume messages:
```commandline
python rmq/main.py direct consume
```

### Fanout Exchange Example:
##### Produce messages:
```commandline
python rmq/main.py fanout produce
```

##### Consume messages:
Default queue is listed as fanout_1

```commandline
python rmq/main.py fanout consume 
```

```commandline
python rmq/main.py fanout consume --queue-name fanout_2
```
