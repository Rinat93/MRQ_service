from core.core_client import SendMessages
from settings.config import *
Client = SendMessages(settings['server'])

SendMessages(settings['server']).send('api2','asf',exchange='logs',exchange_type='topic')
SendMessages(settings['server']).send('api',{"a":2},exchange='logs',exchange_type='topic')
SendMessages(settings['server']).send('rests','asf',exchange='logs',exchange_type='topic')


# from core import BlocRq,MicroRq
# BlocRq(settings['server']).send_queu('api2','asf',exchange='logs',exchange_type='topic')
# BlocRq(settings['server']).send_queu('api','[{"a":2}]',exchange='logs',exchange_type='topic')
# BlocRq(settings['server']).send_queu('rests','Uguguugu',exchange='logs',exchange_type='topic')

# MicroRq('localhost').send_queu('users.mig','asd 2',exchange='logs',exchange_type='topic')
# MicroRq('localhost').send_queu('admin.mig2','admin',exchange='logs',exchange_type='topic')
# MicroRq('localhost').send_queu('users2','sad  2',exchange='logs2',exchange_type='direct')