from dispatch.service import CreateService,run

class B(CreateService):
    service = 'api'

    def context(self,*args,**kwargs):
        context =super(B,self).context(*args,**kwargs)
        print(context)

class C(CreateService):
    service = 'api2'

    def context(self,*args,**kwargs):
        context = super(C,self).context(*args,**kwargs)
        print(context)

if __name__ == '__main__':
    run()