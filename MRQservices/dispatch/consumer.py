from .base.meta_service import *
from threading import Thread

# Объект слушателей
class Consumer(Service):
    __service__ = 'consumer'
    hosts = settings['server']
    exchange = settings['exchange']
    type_exchange = None
    route = None
    queue = None
    callback = None

    # Инициализируем слушателей и потом регистрируем
    def initialize(self,hosts,exchange,type_exchange,route,callback,queue='',*args,**kwargs):
        self.hosts = hosts
        self.exchange = exchange
        self.type_exchange = type_exchange
        self.route = route
        self.queue = queue
        self.callback = callback
        self.__register_consumer()

    # Регистрация слушателей
    def __register_consumer(self):
        Thread(target=MicroRq(self.hosts, self.exchange).run,
               args=(self.callback, self.route, self.queue), kwargs={'exh_type': self.type_exchange}).start()



    # Вывод всех сервисов(регистрирует новые сервисы в других сервисах)
    def _systems_all(cls, ch, method, properties, body):
        body = json.loads(body)
        if body not in cls.register_servce_info:
            print(f"Зарегистрирован сервис: {body}")
            cls.send_message(cls._regisers, cls._service_host)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # else:
            #     ch.basic_cancel(delivery_tag=method.delivery_tag)
            cls.register_servce_info.append(body)
        else:
            print("Уже зарегистрирован")
            ch.basic_ack(delivery_tag=method.delivery_tag)

