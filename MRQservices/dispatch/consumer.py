import json
from .base.meta_service import *
from MRQservices.decoratos.logs import loggigs_service
from MRQservices.core.aio_pika.aio_server import Base
from threading import Thread
import asyncio
# Объект слушателей
class Consumer(Service):
    __service__ = 'consumer'
    hosts = RABBITMQ
    exchange = EXCHANGE
    type_exchange = None
    route = None
    queue = None
    callback = None

    # Инициализируем слушателей и потом регистрируем
    async def initialize(self,hosts,exchange,type_exchange,route,callback,queue='',*args,**kwargs):
        self.hosts = hosts
        self.exchange = exchange
        self.type_exchange = type_exchange
        self.route = route
        self.queue = queue
        self.callback = callback
        Thread(target=self.__register_consumer,args=(hosts,exchange,type_exchange,route,queue,callback)).start()


    # Регистрация слушателей
    def __register_consumer(self,hosts,exchange,type_exh,route,queue,callback):
        mess = Base(hosts,route,exchange,type_exh,queue=queue)
        asyncio.run(mess.run_consumer(callback))

    # Вывод всех сервисов(регистрирует новые сервисы в других сервисах)
    # @loggigs_service
    async def _systems_all(cls, ctx):
        body = ctx.body
        body = json.loads(body)
        if body not in cls.register_servce_info:
            print(f"Зарегистрирован сервис: {body}")
            await cls.send_message(cls._registers, cls._route)
            await cls.send_message({'test':'sdad'}, 'api')
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            # else:
            #     ch.basic_cancel(delivery_tag=method.delivery_tag)
            cls.register_servce_info.append(body)
        else:
            print("Уже зарегистрирован")
            # ch.basic_ack(delivery_tag=method.delivery_tag)

