import json
import re
from MRQservices.dispatch.base.base_service import ServiceBase

class CreateService(ServiceBase):
    __run__ = False
    __service__ = 'sad'

    def __init__(self,*args,**kwargs):
        super(CreateService,self).__init__(*args,**kwargs)


    # Потверждаем о успешном получении(basic_ack) и возвращаем тело сообщения
    def context(self,ch, method, properties, body):
        body = body.decode('utf-8')
        if self.json_serialize(body):
            body = json.loads(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return body

    # Стартуем приложение запуская экземпляры всех зарегистрированных сервисов
    def run(cls):
        cls._send_register_Service()
        if cls.__run__ == False:
            for obj in cls.registry:
                obj()
        else:
            raise Exception("In start")

def run():
    CreateService().run()