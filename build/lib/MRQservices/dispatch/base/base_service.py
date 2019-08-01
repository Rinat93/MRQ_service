from .meta_service import *
# Базовый класс реализирующий регистрацию роутеров
ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"
class ServiceBase(metaclass=ServiceMeta):
    __settings = os.environ.get('SETTINGS_MODULE', None)
    __regisers__ = settings["REGISTER"]
    hosts = settings['server']
    exchange = settings['exchange']
    __service_host = settings['service_host']
    # Что-бы предотвратить повторный запуск экземпелятров сервисов - указываем состояние
    __global_service_start = False
    service_start = False
    __service__ = 'system'

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
        if cls.__global_service_start == False:
            print(1)
            Thread(target=MicroRq(cls.hosts, cls.exchange).run,
                   args=(cls.__systems_all, cls.__service_host, '')).start()
            SendMessages(cls.hosts).send(cls.__service_host, cls.__regisers__, exchange=cls.exchange,
                                         exchange_type='topic')
            cls.__global_service_start = True

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

    def send_message(cls, body, route):
        print(body)
        SendMessages(cls.hosts).send(route, body, exchange=cls.exchange, exchange_type='topic')

    # Сериализация json данных
    def json_serialize(self, body):
        return re.search(r"^{.*}|^\[.*\]", body)

    # Вывод всех сервисов(регистрирует новые сервисы)

    def __systems_all(cls, ch, method, properties, body):
        body = json.loads(body)
        cls.send_message("Я тута", "api")
        # if body['KEY'] == cls.__regisers__["KEY"]:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # else:
        #     ch.basic_cancel(delivery_tag=method.delivery_tag)

    # Регистрация сервисов
    def __register_service__(cls, obj):
        if hasattr(obj, 'service') and obj.service_start == False:
            obj.service_start = True
            Thread(target=MicroRq(obj.hosts, obj.exchange).run, args=(obj.context, obj.service, '')).start()

    def context(self, *args, **kwargs): pass
