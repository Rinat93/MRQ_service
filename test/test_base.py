from MRQservices.core import MicroRq
from MRQservices.dispatch import service
import json
import asyncio
from MRQservices.dispatch.consumer import Consumer,SendMessages
from MRQservices.settings.test_settings import *
import sys
import pytest

class TestBase(object):
    register_servce_info = []

    def points(cls, ch, method, properties, body):
        body = json.loads(body)

        res = {
            'TEST': True
        }
        assert body == res
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return body
        # sys.exit()

    def send_message(cls, body, route, exchange=''):
        SendMessages(config.RABBITMQ).send(route, body, exchange=config.EXCHANGE, exchange_type='direct')

    def test_register_Service(cls):
        # h = MicroRq(config.RABBITMQ, config.EXCHANGE)
        # servers = asyncio.run(h.run(cls.send_message,'direct',config.SERVICE_HOST))
        # print(servers)
        Consumer().initialize(config.RABBITMQ, config.EXCHANGE, 'direct', config.SERVICE_HOST, cls.points, queue='')
        cls.send_message({
            'TEST': True
        },config.SERVICE_HOST)

    def setup(cls):
        cls.test_register_Service()

# print('тут')
if __name__ == '__main__':
    TestBase().setup()