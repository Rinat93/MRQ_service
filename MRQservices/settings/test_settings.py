from MRQservices.settings import config

config.RABBITMQ = 'amqp://guest:guest@localhost:5672/%2F'
config.EXCHANGE = 'test2'
config.SERVICE_HOST = 'test.view'
config.SERVICE_NAME = 'PPC'
config.SERVICE_KEY = '1111'