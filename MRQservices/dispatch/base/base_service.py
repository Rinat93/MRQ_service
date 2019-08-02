from .meta_service import *

# Базовый класс реализирующий регистрацию роутеров
class ServiceBase(metaclass=ServiceMeta):
    hosts = settings['server']
    exchange = settings['exchange']
    register_servce_info = [] # Зарегистрированные сервисы
    __settings = os.environ.get('SETTINGS_MODULE', None)
    __regisers__ = settings["REGISTER"]
    __service_host = settings['service_host']
    # Что-бы предотвратить повторный запуск экземпелятров сервисов - указываем состояние
    service_start = False
    __global_service_start = False
    __service__ = 'system'
    __messages__ = SendMessages(hosts)

    def __new__(cls, *args, **kwargs):
        if cls.__settings:
            settings = importlib.import_module(cls.__settings)
            cls.settings_customs(cls,settings)

        return super().__new__(cls)

    def __init__(cls, *args, **kwargs):
        '''
        Регистрируем все сервисы при старте приложения, регистрируем только те у кого есть
        аттрибут service.
        :param args:
        :param kwargs:
        '''

        # Иниациализируем сервис и отправляем сообщение все сервисам
        '''
            ToDo: Каждый новый сервис имеет __global_service_start = False
                Либо так и оставить, тем самым регистрировать каждый маршрут а не сервис 
                либо придумать симофор...
        '''



    # Если есть enviromen SETTINGS_MODULE тогда кастомизируем настройки
    def settings_customs(cls, settings):
        if hasattr(settings, 'HOST_RABBITMQ'):
            cls.hosts = settings.HOST_RABBITMQ
        if hasattr(settings, 'EXCHANGE'):
            cls.exchange = settings.EXCHANGE
        if hasattr(settings, 'HOST_SERVICE'):
            cls.__service_host = settings.HOST_SERVICE
        if hasattr(settings, 'SERVICE_NAME'):
            cls.__regisers__['SERVICE'] = settings.SERVICE_NAME
        if hasattr(settings, 'SERVICE_KEY'):
            cls.__regisers__['KEY'] = settings.SERVICE_KEY

    # Отправка сообщении в другие сервисы
    def send_message(cls, body, route):
        SendMessages(cls.hosts).send(route, body, exchange=cls.exchange, exchange_type='topic')

    # Сериализация json данных
    def json_serialize(self, body):
        return re.search(r"^{.*}|^\[.*\]", body)

    # Вывод всех сервисов(регистрирует новые сервисы в других сервисах)
    def __systems_all(cls, ch, method, properties, body):
        body = json.loads(body)
        print("AUTH-----")
        print(body)
        print("AUTH.")
        if body not in cls.register_servce_info:
            print(f"Зарегистрирован сервис: {body}")
            cls.send_message(cls.__regisers__, cls.__service_host)
            if body['KEY'] == cls.__regisers__["KEY"]:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_cancel(delivery_tag=method.delivery_tag)
            cls.register_servce_info.append(body)
        else:
            print("Уже зарегистрирован")

    # Создание каналов
    @staticmethod
    def _create_channels(hosts,exchange,callback,host_service,exh_type,queue=''):
        Thread(target=MicroRq(hosts, exchange).run,
               args=(callback, host_service,queue),kwargs={'exh_type':exh_type}).start()

    # Отправка сообщении для регистрации сервиса
    def _send_register_Service(cls):
        if cls.__global_service_start == False:
            cls._create_channels(cls.hosts,cls.exchange,cls.__systems_all,cls.__service_host,'topic')
            cls.send_message(cls.__regisers__,cls.__service_host)
            cls.__global_service_start = True

    # Регистрация сервисов
    def __register_service__(cls, obj):
        if hasattr(obj, 'service') and obj.service_start == False:
            obj.service_start = True
            cls._create_channels(obj.hosts, obj.exchange,obj.context, obj.service,'topic')
            # Thread(target=MicroRq(obj.hosts, obj.exchange).run, args=(obj.context, obj.service, '')).start()

    def context(self, *args, **kwargs): pass


    # def __init_subclass__(self):
    #     self.__global_service_start = True