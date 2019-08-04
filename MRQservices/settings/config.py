import os
RABBITMQ = os.environ.get('RABBITMQ','amqp://guest:guest@localhost:5672/%2F')
EXCHANGE = os.environ.get('EXCHANGE','init')
SERVICE_HOST = os.environ.get('SERVICE_HOST','systems.all')
REGISTER = {
    "KEY": "Q523_Ma",
    "SERVICE": os.environ.get('SERVICE_NAME',"AUTH")
}