# from core import MicroRq
import os

settings={
    'server': os.environ.get('RABBITMQ','amqp://guest:guest@localhost:5672/%2F'),
    'exchange': os.environ.get('EXCHANGE','init'),
    'service_host': os.environ.get('SERVICE_HOST','systems.all'), # Главный канал сервисов
    'REGISTER': {
        "KEY": "Q523_Ma",
        "SERVICE": os.environ.get('SERVICE_NAME',"AUTH") # Название сервиса для его индентификации
    }
}