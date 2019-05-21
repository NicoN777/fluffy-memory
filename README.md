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
### Direct Exchange Example:
##### Send messages to queue bound to a direct exchange:
```commandline
python rmq/main.py --type direct --action produce
```

##### Consume messages:
```commandline
python rmq/main.py --type direct --action consume
```

### Fanout Exchange Example:
##### Produce messages:
```commandline
python rmq/main.py --type fanout --action produce
```

##### Consume messages:
```commandline
python rmq/main.py --type fanout --action consume
```
