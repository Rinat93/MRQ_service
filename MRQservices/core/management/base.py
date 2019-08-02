import os
import argparse
import importlib
from setuptools import Command
from MRQservices.core.core_client import SendMessages


class BaseCommand:
    name_services = None

    def __init__(self,*args,**kwargs):
        parser = argparse.ArgumentParser(description='Add some integers.')
        self.add_arguments(parser)

    def add_arguments(self, parser):

        parser.add_argument('--host', metavar='host', type=str, nargs=1,
                            help='Хост Rabbitmq по умолчанию: amqp://guest:guest@localhost:5672/%2F',default='amqp://guest:guest@localhost:5672/%2F')
        parser.add_argument('--route', metavar='Router/Binding', default='systems.*', help='Укажите маршрут для сообщения')
        parser.add_argument('--body', metavar='Body', help='Сообщение')
        parser.add_argument('--exchange', metavar='Exchange', help='Название точки обмена', default='logs')
        parser.add_argument('--exchange_type', metavar='Exchange type', help='Название типа маршрута', default='topic')
        args = parser.parse_args()
        if args.body:
            self.sendMessage(args.host,args.route,args.body,args.exchange,args.exchange_type)

    def sendMessage(self,host,route,body,exchange,exchange_type):
        SendMessages(host).send(route, body, exchange=exchange, exchange_type=exchange_type)

    def handle(self, *args,**kwargs):
        if not self.name_services:
            raise Exception("Не указали имя сервиса (параметр name)")
        app = self.name_services

        if not os.path.isdir(app):
            os.makedirs(app)
        for i in os.walk(os.getcwd()+'/templates'):
            print(i)