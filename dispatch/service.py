import json
import re
from dispatch.base.base_service import ServiceBase,logging

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


    # Сериализация json данных
    def json_serialize(self,body):
        return re.search(r"^{.*}|^\[.*\]",body)

    # Стартуем приложение запуская экземпляры всех зарегистрированных сервисов
    def run(cls):
        if cls.__run__ == False:
            for obj in cls.registry:
                obj()
        else:
            raise Exception("In start")

def run():
    CreateService().run()