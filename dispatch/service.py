from dispatch.base.base_service import ServiceBase

class CreateService(ServiceBase):
    __service__ = 'sad'

    def __init__(self,*args,**kwargs):
        super(CreateService,self).__init__(*args,**kwargs)

    def context(self):
        pass
