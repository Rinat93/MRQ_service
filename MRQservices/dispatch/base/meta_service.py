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
class ServiceMeta(type):

    def __new__(cls, name, bases, nmspc):
        nmspc['__call__'] = cls.__call__

        # должно быть имя сервиса и его контекст(callback)
        if (not 'service' in nmspc and not '__service__' in nmspc):
            raise Exception('Not name service!')

        if (not 'context' in nmspc):
            raise Exception('Not context service')

        return super().__new__(cls, name, bases, nmspc)

    def __init__(cls, *args, **kwargs):

        if not hasattr(cls, 'registry'):
            cls.registry = set()

        if hasattr(cls, 'service'):
            cls.registry.add(cls)
        return super().__init__(*args,**kwargs)

    def __call__(self, *args, **kwargs):
        call = super().__call__(*args, **kwargs)
        self.__register_service__(self,call)
        return call


