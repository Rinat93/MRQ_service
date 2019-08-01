# import log

from MRQservices.core.core_client import SendMessages
from MRQservices.settings.config import settings
from MRQservices.core import MicroRq
from threading import Thread
import importlib
import os
import re
import json
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
'''
    cls - объект который наследуется от данного класса либо класса который является
        прям наследником данного мета класса
    name - имя класса
    bases - тот же объект только в кортеже
    nmspc - структу наследного класса (название модуля откуда произошел вызов, его имя и методы и аттрибуты)
    ------------------
    *args - вся информация об наследуемом объекте, его методы, аргументы и др
    exchange - Имя точки обмена
'''
ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"
class ServiceMeta(type):
    __service__ = None
    __settings = os.environ.get('SETTINGS_MODULE',None)
    __regisers__ = settings["REGISTER"]
    hosts = settings['server']
    exchange = settings['exchange']
    __service_host = settings['service_host']
    # Что-бы предотвратить повторный запуск экземпелятров сервисов - указываем состояние
    __global_service_start = False
    service_start = False

    def settings_customs(cls,settings):
        if hasattr(settings,'HOST_RABBITMQ'):
            cls.hosts = settings.HOST_RABBITMQ
        if hasattr(settings,'EXCHANGE'):
            cls.exchange = settings.EXCHANGE
        if hasattr(settings,'HOST_SERVICE'):
            cls.__service_host = settings.HOST_SERVICE
        if hasattr(settings,'SERVICE_NAME'):
            cls.__regisers__['SERVICE'] = settings.SERVICE_NAME
        if hasattr(settings,'SERVICE_KEY'):
            cls.__regisers__['KEY'] = settings.SERVICE_KEY

    def __new__(cls, name, bases, nmspc):
        # Если есть enviromen SETTINGS_MODULE тогда кастомизируем настройки
        if cls.__settings:
            settings = importlib.import_module(cls.__settings)
            cls.settings_customs(cls,settings)

        # должно быть имя сервиса и его контекст(callback)
        if (not 'service' in nmspc and not '__service__' in nmspc):
            raise Exception('Not name service!')

        if (not 'context' in nmspc):
            raise Exception('Not context service')

        # Всем определяем родительское событие вызова объекта
        nmspc['__call__'] = cls.__call__

        return super(ServiceMeta, cls).__new__(cls, name, bases, nmspc)

    def send_message(cls,body,exchange):
        SendMessages(cls.hosts).send(cls.__service_host,body, exchange=exchange, exchange_type='topic')


    # Сериализация json данных
    def json_serialize(self,body):
        return re.search(r"^{.*}|^\[.*\]",body)

    # Вывод всех сервисов(регистрирует новые сервисы)

    def __systems_all(cls,ch, method, properties, body):
        # cls.send_message("Я тута","api")
        body = json.loads(body)
        print(body)
        if body['KEY'] == cls.__regisers__["KEY"]:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_cancel(delivery_tag=method.delivery_tag)


    # Регистрация сервисов
    def __register_service__(cls):
        if cls.__global_service_start  == False:
            Thread(target=MicroRq(cls.hosts, cls.exchange).run, args=(cls.__systems_all, cls.__service_host, '')).start()
            SendMessages(cls.hosts).send(cls.__service_host,cls.__regisers__, exchange=cls.exchange, exchange_type='topic')
            cls.__global_service_start  = True

        if hasattr(cls,'service') and cls.service_start == False:
            cls.service_start = True
            Thread(target=MicroRq(cls.hosts, cls.exchange).run, args=(cls().context,cls.service,'')).start()


    def __init__(cls, *args,**kwargs):
        '''
        Регистрируем все сервисы при старте приложения, регистрируем только те у кого есть
        аттрибут service.
        :param args:
        :param kwargs:
        '''
        if not hasattr(cls, 'registry'):
            cls.registry = set()

        if hasattr(cls, 'service'):
            cls.registry.add(cls)

        super(ServiceMeta, cls).__init__(*args,**kwargs)

    def __call__(self, *args, **kwargs):
        self.__register_service__()
        return super(ServiceMeta,self).__call__(*args,**kwargs)

    def context(cls):pass

    def __iter__(cls):
        return iter(cls.registry)

# Базовый класс реализирующий регистрацию роутеров
class ServiceBase(metaclass=ServiceMeta):
    __service__ = 'system'

    def __new__(cls,  *args,**kwargs):
        return super(ServiceBase, cls).__new__(cls, *args,**kwargs)

    def __init__(cls,*args,**kwargs):
        super(ServiceBase, cls).__init__(*args,**kwargs)

    def context(self,ch, method, properties, body):pass



