import asyncio
from MRQservices.core.aio_pika.aio_server import Base
from MRQservices.settings.test_settings import *
import pytest
import json
import sys

mess = Base(config.RABBITMQ,config.SERVICE_HOST,config.EXCHANGE,'direct',queue='')
class TestBase(object):
    register_servce_info = []

    async def points(cls, ctx):
        res = json.loads(ctx.body.decode())
        assert res == {
            'TEST': True
        }
        print(ctx)
        # ctx.conn.close()

    async def send_message(cls, body, route, exchange=''):
        mess = Base(config.RABBITMQ,route,exchange,'direct')
        await mess.run_publisher(body)

    def run_consumer(cls):
        mess = Base(config.RABBITMQ,config.SERVICE_HOST,config.EXCHANGE,'direct',queue='')
        asyncio.run(mess.run_consumer(cls.points))

    async def register_Service(cls,loop):
        await mess.run_consumer(cls.points,loop)

    async def send(cls,loop):
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
        pass
        # asyncio.run()

# print('тут')
# if __name__ == '__main__':
#     TestBase().setup()