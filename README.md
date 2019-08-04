Фреймворк для простой рзработки web приложении с полной поддержкой микросервисной
архитектурой, взаимодействия между сервисами происходить через брокер задач Rabbitmq
и драйвер aio-pika(https://github.com/mosquito/aio-pika).
Не для production!

## Описание настроек
    SETTINGS_MODULE=settings.config - подключение файла с настройками
    HOST_RABBITMQ = 'amqp://guest:guest@localhost:5672/%2F'
    EXCHANGE = 'EXCHANGE_EXAMPLE'
    HOST_SERVICE = 'HOST.EXAMPLE'
    SERVICE_NAME = 'NAME_EXAMPLE'
    SERVICE_KEY = 'KEY_EXAMPLE'
    
    либо изменение параметров "напрямую"
    from MRQservices.settings import config
    config.HOST_RABBITMQ = ***
    ... etc.

## Примеры
    Пример реализации микросервиса
    from MRQservices.dispatch.service import CreateService,run
    
    class EXAMPLE(CreateService):
        service = 'SERVICE_NAME' # Exchange
        await self.send_message('body','route',exchange_type='direct') # отправка сообщения
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
        
        async def context(self,*args,**kwargs):
            context = super(EXAMPLE,self).context(*args,**kwargs)
    
    if __name__ == '__main__':
        run() 
        
Так же есть возможность создавать сервисы при помощи декораторов

    from MRQservices.decoratos.create_microservice import Microservise
    from MRQservices.dispatch.service import run
    
    @Microservise()
    async def rests(ctx):
        print(1)
        print(ctx.body)
        
    @Microservise(route='api2')
    async def asa(ctx):
        print(2)
        print(ctx.body)
    
    @Microservise(route='api')
    async def callback(ctx):
        print(3)
        print(ctx.body)
    
    if __name__ == '__main__':
        run()
        
# Немного о работе

    Каждый новый сервис добавляется в глобальный "стек" объекта для последующего ее 
    инициализации и регистрации, так-что при первом запуске все сервисы отправять друг
    другу сообщение для подтверждения что все работает корректно на этапе старта.
    
# Планы

    Из-за довольно интенсивной смены подходов разработки код стал немного запутаным
    потому первое в планах оптимизировать всю центральную часть "ядра" т.к. изначально
    писался на основе официального драйвера pika и из-за ее низкой эффективности
    пришлось переехать на aio-pika.
    
    2. Сделать хранилище для всех зарегистрированных сервисов что-бы при
    перезапуске не приходолись ждать пока каждый сервис ответит
    
    3. Централизированное управление всеми сервисами(внезависимости от яп),
        контроль логов, тестировать api/socket/каналы через интерфейс и видеть 
        любой отказ сервиса, так-же перезапуск и остановка сервиса
        
    ...