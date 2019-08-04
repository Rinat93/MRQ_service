from MRQservices.settings import config

config.RABBITMQ = 'amqp://guest:guest@localhost:5672/%2F'
config.EXCHANGE = 'logs'
config.SERVICE_HOST = 'systems.view'
config.SERVICE_NAME = 'PPC'
config.SERVICE_KEY = '1111'