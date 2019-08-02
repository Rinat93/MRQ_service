from MRQservices.dispatch.service import CreateService,run
#SETTINGS_MODULE
class B(CreateService):
    service = 'api'

    def context(self,*args,**kwargs):
        context =super(B,self).context(*args,**kwargs)

class C(CreateService):
    service = 'api2'

    def context(self,*args,**kwargs):
        context = super(C,self).context(*args,**kwargs)

if __name__ == '__main__':
    run()