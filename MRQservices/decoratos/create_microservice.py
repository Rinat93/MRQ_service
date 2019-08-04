import MRQservices.log as log
from MRQservices.core.aio_pika.aio_server import Base
from MRQservices.settings import config
from threading import Thread
import asyncio

class Microservise(object):

    def __init__(self,*args,**kwargs):
        if len(args)>0:
            self.func = args[0]
        self.route = kwargs.get('route')

    def create_microservice(self,func,route):
        mess = Base()
        mess.ROUTING_KEY = route
        mess.EXCHANGE_TYPE = 'topic'
        mess.EXCHANGE = config.EXCHANGE
        asyncio.run(mess.run_consumer(func))

    def __call__(self,*args,**kwargs):
        funct = None
        if len(args) > 0:
            if not self.route:
                self.route = args[0].__name__
            funct = args[0]
        elif hasattr(self,'func'):
            if not self.route:
                self.route = self.func.__name__
            funct = self.func
        else:
            raise Exception("Not decorator")
        Thread(target=self.create_microservice, args=(funct,self.route)).start()