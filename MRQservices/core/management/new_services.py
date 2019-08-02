from io import TextIOBase
import os
import importlib
importlib.import_module()
class BaseCommand:
    name_services = None

    def __init__(self,*args,**kwargs):
        self.name_services = os.environ.get('name',None)
        self.handle()

    def add_arguments(self, parser):
        parser.add_argument('name', help='Название сервиса.')

    def handle(self, *args,**kwargs):
        if not self.name_services:
            raise Exception("Не указали имя сервиса (параметр name)")
        app = self.name_services

        if not os.path.isdir(app):
            os.makedirs(app)

        print("Привет")

        print(os.getcwd())
        for i in os.walk(os.getcwd()+'/templates'):
            print(i)