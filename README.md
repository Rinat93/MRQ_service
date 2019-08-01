Фреймворк для простой рзработки web приложении с полной поддержкой микросервисной
архитектурой, взаимодействия между сервисами происходить через брокер задач Rabbatmq
и официальный драйвер pika.

## Описание настроек
    SETTINGS_MODULE=settings.config - подключение файла с настройками
    HOST_RABBITMQ = 'amqp://guest:guest@localhost:5672/%2F'
    EXCHANGE = 'EXCHANGE_EXAMPLE'
    HOST_SERVICE = 'HOST.EXAMPLE'
    SERVICE_NAME = 'NAME_EXAMPLE'
    SERVICE_KEY = 'KEY_EXAMPLE'

## Примеры
    Пример реализации микросервиса
    from MRQservices.dispatch.service import CreateService,run
    
    class EXAMPLE(CreateService):
        service = 'SERVICE_NAME' # Exchange
        ''' 
            После того как какой либо сервис отправить сообщение в
            данный сервис(имя задается в service) это сообщение попадает
            в context потому этот метод обязательно следует описать.
            В context попадают след. аргументы:
            canal - канал(смотрите документацию pika)
            method - метод(смотрите документацию pika)
            properties - настройки(смотрите документацию pika)
            body - сообщение(либо json либо text)
        '''
        
        def context(self,*args,**kwargs):
            context = super(EXAMPLE,self).context(*args,**kwargs)
    
    if __name__ == '__main__':
        run() 
     