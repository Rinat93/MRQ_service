from dispatch.service import CreateService

class B(CreateService):
    service = 'home'

    def context(self):
        print("test")

B()