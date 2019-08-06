import os
RABBITMQ = os.environ.get('RABBITMQ','amqp://guest:guest@localhost:5672/%2F')
EXCHANGE = os.environ.get('EXCHANGE','init')
ROUTE = os.environ.get('SERVICE_HOST','systems.all')
EXCHANGE_TYPE = 'topic'
REGISTER = {
    "KEY": "Q523_Ma",
    "SERVICE": os.environ.get('SERVICE_NAME',"AUTH")
}