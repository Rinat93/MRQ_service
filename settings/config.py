from core import MicroRq
import os

settings = None #os.environ.get('MSQ_SETTINGS')
class Settings(object):

    @staticmethod
    def init():
        settings = {
            'server': 'localhost',
            'exchange': 'logs'
        }
        return settings

settings = Settings.init()