import asyncio
from MRQservices.core.aio_pika.aio_server import Base
from MRQservices.settings.test_settings import *
import pytest

class TestBase(object):
    register_servce_info = []

    async def points(cls, body):
        print("Тута")
        print(body)
        # sys.exit()

    async def send_message(cls, body, route, exchange=''):
        mess = Base()
        mess.ROUTING_KEY = route
        mess.EXCHANGE = exchange
        await mess.run_publisher(body)

    def run_consumer(cls):
        mess = Base()
        mess.ROUTING_KEY = config.SERVICE_HOST
        mess.EXCHANGE_TYPE = 'direct'
        mess.EXCHANGE = config.EXCHANGE
        asyncio.run(mess.run_consumer(cls.points))

    async def register_Service(cls,loop):
        mess = Base()
        mess.ROUTING_KEY = config.SERVICE_HOST
        mess.EXCHANGE_TYPE = 'direct'
        mess.EXCHANGE = config.EXCHANGE
        await mess.run_consumer(cls.points,loop)
        print('Тут')

    async def send(cls,loop):
        # Thread(target=cls.run_consumer,args=()).start()
        await cls.send_message({
            'TEST': True
        },config.SERVICE_HOST,loop)

    def test_start(cls):
        loop = asyncio.get_event_loop()
        gr = asyncio.gather(
            cls.register_Service(loop),
            cls.send(loop)
        )
        loop.run_until_complete(gr)
        loop.close()

    def setup(cls):
        loop = asyncio.get_event_loop()
        gr = asyncio.gather(
            cls.register_Service(loop),
            cls.send(loop)
        )
        loop.run_until_complete(gr)
        loop.close()
        # asyncio.run()

# print('тут')
# if __name__ == '__main__':
#     TestBase().setup()