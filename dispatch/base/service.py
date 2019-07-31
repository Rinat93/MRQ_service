# import log
# from core import MicroRq,BlocRq
from settings.config import *
# import asyncio
# from threading import Thread

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
    hosts = settings['server']
    exchange = settings['exchange']

    def __new__(cls, name, bases, nmspc):
        return super(ServiceMeta, cls).__new__(cls, name, bases, nmspc)

    def __init__(cls, *args,**kwargs):
        if not hasattr(cls, 'registry'):
            # все зарегистрированные объекты
            cls.registry = set()

        if hasattr(cls, 'name'):
            cls.registry.add(cls)
        super(ServiceMeta, cls).__init__(*args,**kwargs)

    def __iter__(cls):
        return iter(cls.registry)

# Базовый класс реализирующий регистрацию роутеров
class ServiceBase(metaclass=ServiceMeta):
    def __new__(cls,  *args,**kwargs):
        if not hasattr(cls, 'name'):
            raise Exception('Not name service!')
        return super(ServiceBase, cls).__new__(cls, *args,**kwargs)

    def __init__(cls,*args,**kwargs):
        super(ServiceBase, cls).__init__(*args,**kwargs)

    def names(self,name):
        pass


class A(ServiceBase):
    name = 'sad'

class B(A):
    pass
# print(A.name)
print(A().registry)