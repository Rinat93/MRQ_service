from MRQservices.dispatch import service
import json
from MRQservices.settings.test_settings import *
import unittest


class TestBase(service.CreateService):

    def test_point(cls, ch, method, properties, body):
        body = json.loads(body)
        if body not in cls.register_servce_info:
            print(f"Тестовые данные: {body}")
            cls.send_message(cls._registers, cls._service_host)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # else:
            #     ch.basic_cancel(delivery_tag=method.delivery_tag)
            cls.register_servce_info.append(body)
            assert "Успешно пройдено"
        else:
            print("Уже зарегистрирован")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def _send_register_Service(cls):
        print("Запуск")
        if cls.__global_service_start == False:
            cls._create_channels(cls.hosts,cls.exchange,cls.test_point,cls._service_host,'topic')
            cls.send_message({
                'TEST': True
            },cls._service_host)
            cls.__global_service_start = True

    def test_run(cls):
        cls._send_register_Service()
print('тут')
if __name__ == '__main__':
    TestBase().test_run()