import log
from core import MicroRq
from settings.config import *
import asyncio

Servers = MicroRq(settings['server'])
Exchange = settings['exchange']

class Microservise(object):
    
    def __init__(self,*args,**kwargs):
        if len(args)>0:
            self.func = args[0]
        self.route = kwargs.get('route')

    async def create_microservice(self,func,route):
        print(func.__name__)
        await Servers.subscribe(Exchange,func,routing_key=route or func.__name__,exchange_type='direct')

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
        
        asyncio.run(self.create_microservice(funct,self.route))