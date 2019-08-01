from dispatch.base.base_service import ServiceBase,logging

class CreateService(ServiceBase):
    __run__ = False
    __service__ = 'sad'

    def __init__(self,*args,**kwargs):
        super(CreateService,self).__init__(*args,**kwargs)

    def context(self,ch, method, properties, body):
        # print(len(args))
        # ch = args[0]
        # method = args[1]
        # properties = args[2]
        # body = args[3]
        ch.basic_ack(delivery_tag=method.delivery_tag)

        return body

    def run(cls):
        # logging.DEBUG('Start server: ')
        if cls.__run__ == False:
            for obj in cls.registry:
                obj()
        else:
            raise Exception("In start")

def run():
    CreateService().run()