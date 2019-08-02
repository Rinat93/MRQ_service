# import log

from MRQservices.core.core_client import SendMessages
from MRQservices.settings.config import *
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
class ServiceMeta(type):
    __service__ = ''
    def __new__(cls, name, bases, nmspc):
        nmspc['__call__'] = cls.__call__

        # должно быть имя сервиса и его контекст(callback)
        if (not 'service' in nmspc and not '__service__' in nmspc):
            raise Exception('Not name service!')

        if (not 'context' in nmspc and not '__service__' in nmspc):
            raise Exception('Not context service')

        return super().__new__(cls, name, bases, nmspc)

    def __init__(cls, *args, **kwargs):

        if not hasattr(cls, 'registry'):
            cls.registry = set()

        if hasattr(cls, 'service'):
            cls.registry.add(cls)

    def __call__(self, *args, **kwargs):
        call = super().__call__(*args, **kwargs)
        if hasattr(self,'_register_service'):
            self._register_service(self,call)
        return call


# Общий объект для объеденения некоторых методов которые присущи как слушателям так и отправителям
class Service(metaclass=ServiceMeta):
    __service__ = 'meta'
    hosts = RABBITMQ
    exchange = EXCHANGE
    register_servce_info = []  # Зарегистрированные сервисы
    _settings = os.environ.get('SETTINGS_MODULE', None)
    _regisers = REGISTER
    _service_host = SERVICE_HOST
    DEBUG = False

    def __new__(cls, *args, **kwargs):
        if cls._settings:
            settings = importlib.import_module(cls._settings)
            cls.settings_customs(cls, settings)

        return super().__new__(cls)

    # Если есть enviromen SETTINGS_MODULE тогда кастомизируем настройки
    def settings_customs(cls, settings):
        if hasattr(settings, 'HOST_RABBITMQ'):
            cls.hosts = settings.HOST_RABBITMQ
        if hasattr(settings, 'EXCHANGE'):
            cls.exchange = settings.EXCHANGE
        if hasattr(settings, 'HOST_SERVICE'):
            cls.__service_host = settings.HOST_SERVICE
        if hasattr(settings, 'SERVICE_NAME'):
            cls._regisers['SERVICE'] = settings.SERVICE_NAME
        if hasattr(settings, 'SERVICE_KEY'):
            cls._regisers['KEY'] = settings.SERVICE_KEY
        if hasattr(settings, 'DEBUG'):
            cls.DEBUG = settings.DEBUG

        if cls.DEBUG:
            logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT,
                                filename='log/error_' + cls._regisers['SERVICE'] + '.log', filemode='w+')
            logging.basicConfig(level=logging.CRITICAL, format=LOG_FORMAT,
                                filename='log/critical_' + cls._regisers['SERVICE'] + '.log', filemode='w+')
            logging.basicConfig(level=logging.FATAL, format=LOG_FORMAT,
                                filename='log/error_' + cls._regisers['SERVICE'] + '.log', filemode='w+')

    # Отправка сообщении в другие сервисы
    def send_message(cls, body, route, exchange=''):
        print(body)
        SendMessages(cls.hosts).send(route, body, exchange=cls.exchange, exchange_type='topic')

    # Сериализация json данных
    def json_serialize(self, body):
        return re.search(r"^{.*}|^\[.*\]", body)

    def context(self, *args, **kwargs):
        pass

