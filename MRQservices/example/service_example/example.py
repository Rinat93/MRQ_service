from MRQservices.dispatch.service import CreateService,run
#SETTINGS_MODULE
class B(CreateService):
    service = 'api'

    async def context(self,*args,**kwargs):
        await self.send_message('body','route',exchange_type='direct') # отправка сообщения
        context =super(B,self).context(*args,**kwargs)

class C(CreateService):
    service = 'api2'

    async def context(self,*args,**kwargs):
        context = super(C,self).context(*args,**kwargs)

if __name__ == '__main__':
    run()