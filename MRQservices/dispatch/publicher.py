from .consumer import *
# Объект отправителей
class Publisher(Consumer):
    __service__ = 'publisher'
    # Что-бы предотвратить повторный запуск экземпелятров сервисов - указываем состояние
    service_start = False
    __global_service_start = False

    # Создание каналов
    @staticmethod
    def _create_channels(hosts,exchange,callback,host_service,exh_type,queue=''):
        Consumer().initialize(hosts,exchange,exh_type,host_service,callback,queue=queue)

    # Отправка сообщении для регистрации сервиса
    def _send_register_Service(cls):
        if cls.__global_service_start == False:
            cls._create_channels(cls.hosts,cls.exchange,cls._systems_all,cls._service_host,'topic')
            cls.send_message(cls._regisers,cls._service_host)
            print("Tut")
            cls.__global_service_start = True



    # Регистрация сервисов
    def _register_service(cls, obj):
        if hasattr(obj, 'service') and obj.service_start == False:
            obj.service_start = True
            cls._create_channels(obj.hosts, obj.exchange,obj.context, obj.service,'topic')
            # Thread(target=MicroRq(obj.hosts, obj.exchange).run, args=(obj.context, obj.service, '')).start()
