import pika
from core import BlocRq


BlocRq('localhost').send_queu('api','1213asd',exchange='logs',exchange_type='topic')
BlocRq('localhost').send_queu('api2','asf',exchange='logs',exchange_type='topic')

# MicroRq('localhost').send_queu('users.mig','asd 2',exchange='logs',exchange_type='topic')
# MicroRq('localhost').send_queu('admin.mig2','admin',exchange='logs',exchange_type='topic')
# MicroRq('localhost').send_queu('users2','sad  2',exchange='logs2',exchange_type='direct')