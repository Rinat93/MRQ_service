import log
from core import MicroRq,BlocRq
from settings.config import *
import asyncio
from threading import Thread

# micro = MicroRq(settings['server'],settings['exchange'])
# Servers = BlocRq(settings['server'])
Exchange = settings['exchange']

class Microservise(object):

    def __init__(self,*args,**kwargs):
        if len(args)>0:
            self.func = args[0]
        self.route = kwargs.get('route')

    def create_microservice(self,func,route):
        print(route or func.__name__)
        MicroRq(settings['server'], settings['exchange']).run(func,route or func.__name__,'')
        # BlocRq(settings['server']).subscribe(Exchange,func,routing_key=route or func.__name__,exchange_type='topic')
    #

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
