# import log
# from core import MicroRq,BlocRq
from settings.config import settings
from core import MicroRq,BlocRq
from threading import Thread
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
    __service__ = None
    hosts = settings['server']
    exchange = settings['exchange']
    # Что-бы предотвратить повторный запуск экземпелятров сервисов - указываем состояние
    service_start = False

    def __new__(cls, name, bases, nmspc):
        # должно быть имя сервиса и его контекст(callback)
        if (not 'service' in nmspc and not '__service__' in nmspc):
            raise Exception('Not name service!')

        if (not 'context' in nmspc):
            raise Exception('Not context service')

        # Всем определяем родительское событие вызова объекта
        nmspc['__call__'] = cls.__call__

        return super(ServiceMeta, cls).__new__(cls, name, bases, nmspc)


    # Регистрация сервисов
    def __register_service__(cls):
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



