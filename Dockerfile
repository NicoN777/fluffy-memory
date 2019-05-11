FROM rabbitmq:3-management
COPY . /rmq
WORKDIR /rmq
EXPOSE 5672
EXPOSE 15672
CMD ["python", "rmq/main.py"]