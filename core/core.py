import pika

'''
    queue - имя очереди
    exchange_type - [topic,direct,fanout]
    topic - позволяет указывать # и * в именах "канала" тем самым указывая
    что нужно прослушивать, например users.* означает что будет слушать все сообщения
    которые будут отправлять на users.*
'''

class MicroRq(object):
    
    def __init__(self,hosts):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(hosts))
        self.channel = self.connection.channel()

    def create_channels(self,queue,callback,auto_ack=False):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue,auto_ack=auto_ack,on_message_callback=callback)
        self.channel.start_consuming()
    

    '''
        @param exchange - Название канала /{NAME} если он пустой '' тогда берется имя от routing_key
        @param callback - Функция которая должна быть выполнена
        @param routing_key - имя роутера
        @param exchange_type - режим рабоыт слушателя
        @param queue - имя очереди
    '''
    async def subscribe(self,exchange,callback,routing_key='',exchange_type='fanout',queue=''):
        print("Сука я тута")
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        # self.callback = []
        result = self.channel.queue_declare(queue=queue, exclusive=True)
        queue_name = result.method.queue
        if type(routing_key) == list:
            for i in routing_key:
                self.channel.queue_bind(exchange=exchange, queue=queue_name,routing_key=i)
        else:
            self.channel.queue_bind(exchange=exchange, queue=queue_name,routing_key=routing_key)
        self.channel.basic_consume(queue=queue_name, auto_ack=False,on_message_callback=callback)
        self.channel.start_consuming()


    '''
        Если routing_key == '' то сообщение отправится всем наблюдателям
        exchange - между кем будет обмен
    '''
    def send_queu(self,routing_key,body,exchange='',exchange_type='fanout',durable=True):
        self.channel.queue_declare(queue=routing_key, durable=durable)
        
        if exchange != '':
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        
        self.channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=body,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        self.connection.close()
