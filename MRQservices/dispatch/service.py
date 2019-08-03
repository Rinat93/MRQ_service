from .publicher import *
import codecs
class CreateService(Publisher):
    __run__ = False
    __service__ = 'sad'

    def __init__(self,*args,**kwargs):
        super(CreateService,self).__init__(*args,**kwargs)


    # Потверждаем о успешном получении(basic_ack) и возвращаем тело сообщения
    async def context(self,ctx):
        body = ctx.body.decode()
        if await self.json_serialize(body):
            body = json.loads(body)

        # ch.basic_ack(delivery_tag=method.delivery_tag)
        return body

    # Стартуем приложение запуская экземпляры всех зарегистрированных сервисов
    async def run(cls):
        await cls._send_register_Service()
        if cls.__run__ == False:
            for obj in cls.registry:
                # print(obj)
                await cls._register_service(obj())
        else:
            raise Exception("In start")

def run():

    server = CreateService()
    asyncio.run(server.run())