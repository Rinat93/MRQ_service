import functools
import logging
import time
import pika
import os
from .driver_mrq import MRQdriver
'''
    queue - имя очереди
    exchange_type - [topic,direct,fanout]
    topic - позволяет указывать # и * в именах "канала" тем самым указывая
    что нужно прослушивать, например users.* означает что будет слушать все сообщения
    которые будут отправлять на users.*
'''
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

if os.environ.get('debug',False):
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT,filename='log/log_mrq.log')

class MicroRq(object):
    EXCHANGE = 'message'
    EXCHANGE_TYPE = 'topic'
    QUEUE = 'text'
    ROUTING_KEY = 'example.text'

    def __init__(self, amqp_url,exchange):
        """ Создание нового соединения
        URL соединение с Rabbitmq
        :param str amqp_url
        """
        self.should_reconnect = False
        self.was_consuming = False
        self.EXCHANGE = exchange
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1

    def connect(self):
        """
        Соединение с Rabbitmq
        :return:
        """
        LOGGER.info('Connecting to %s', self._url)
        return MRQdriver(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    # Закрытие соединения
    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            LOGGER.info('Connection is closing or already closed')
        else:
            LOGGER.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        """
        Этот метод вызывается когда соединение с RabbitMQ был создан. Он передает дескриптор объекту соединения,
        если нам это нужно, но в этом случае мы просто отметим это как неиспользованное.
        :param pika.SelectConnection _unused_connection: The connection
        """
        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        """Ошибка если соединение небыло установлено
        :param pika.SelectConnection _unused_connection: Объект соединения
        :param Exception err: Ошибка
        """
        LOGGER.error('Connection open failed: %s', err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        """
        Неожиданое закрытие
            :param pika.connection.Connection connection: Объект соединения
            :param Exception reason: Причина закрытия
        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def reconnect(self):
        """Переподключение если не удалось установить соединение либо было закрыто
        """
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        """Открытие нового канала
        """
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """Мето вызывается когда открывается канал
        :param pika.channel.Channel channel: Объект канала
        """
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        """Этот метод указывает на неожиданое закрытие канала
        """
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        """Вызывается когда Rabbitmq закрывает канал
        :param pika.channel.Channel: Закрытий канал
        :param Exception reason: Причина закрытия
        """
        LOGGER.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def setup_exchange(self, exchange_name):
        """Когда канал будет открыть произойдет настройка обмена сообщениями
        :param str|unicode exchange_name: Название обмена
        """

        LOGGER.info('Declaring exchange: %s', exchange_name)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(
            self.on_exchange_declareok, userdata=exchange_name)
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=self.EXCHANGE_TYPE,
            callback=cb)

    def on_exchange_declareok(self, _unused_frame, userdata):
        """Вызывается когда обмен был завершен
        :param pika.Frame.Method unused_frame: Exchange.DeclareOk ответ
        :param str|unicode userdata: Дополнительные данные(обменное имя)
        """
        LOGGER.info('Exchange declared: %s', userdata)
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        """Настройка очереди
        :param str|unicode queue_name: Имя очереди
        """
        LOGGER.info('Declaring queue %s', queue_name)
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb)

    def on_queue_declareok(self, _unused_frame, userdata):
        """ В этом методе мы будем связывать очередь
        и обмен с ключом маршрутизации путем выдачи Queue.Bind.
        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        queue_name = userdata
        LOGGER.info('Binding %s to %s with %s', self.EXCHANGE, queue_name,
                    self.ROUTING_KEY)
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def on_bindok(self, _unused_frame, userdata):

        """Вызывается pika после завершения метода Queue.Bind. В этот
        Точка мы будем устанавливать количество предварительной выборки для канала.
        :param pika.frame.Method _unused_frame: The Queue.BindOk response frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        LOGGER.info('Queue bound: %s', userdata)
        self.set_qos()

    def set_qos(self):
        """
        Этот метод устанавливает предварительную выборку потребителя только для доставки
        одно сообщение за раз. Потребитель должен подтвердить это сообщение
        прежде чем RabbitMQ доставит еще один. Вы должны экспериментировать
        с различными значениями предварительной выборки для достижения желаемой производительности.
        """
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        """Вызывается после завершения метода Basic.QoS.
        Здесь мы начнем потреблять сообщения, вызывая start_consuming
        который вызовет необходимые команды RPC для запуска процесса.
        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame
        """
        LOGGER.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        """
        Этот метод настраивает потребителя первым вызовом
        add_on_cancel_callback, так что объект уведомляется если RabbitMQ
        отменяет потребителя. Затем он запускает команду Basic.Consume RPC
        который возвращает потребительский тег, который используется для уникальной идентификации
        потребителя с RabbitMQ. Мы сохраняем ценность, чтобы использовать его, когда мы хотим
        отменить потребление. Метод callback передается как обратный вызов когда сообщение будет полностью получено.
        """
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.callback)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        """Добавьте обратный вызов, который будет вызван, если RabbitMQ отменяет потребителя
        по какой-то причине. Если RabbitMQ действительно отменяет потребителя,
        on_consumer_cancelled будет вызываться.
        """
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Вызывается когда происходить отмена от потребителя
        :param pika.frame.Method method_frame: The Basic.Cancel frame
        """
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()
    
    # def on_message(self, _unused_channel, basic_deliver, properties, body):
    #     """
    #     Вызывается pika при доставке сообщения из RabbitMQ.
    #     канал пропущен для вашего удобства. Объект basic_deliver, который
    #     передается в обмен, ключ маршрутизации, тег доставки и
    #     доставленный флаг для сообщения. Свойства, переданные в это
    #     экземпляр BasicProperties со свойствами сообщения и телом
    #     это сообщение, которое было отправлено.
    #     :param pika.channel.Channel _unused_channel: Канал
    #     :param pika.Spec.Basic.Deliver: basic_deliver Метод
    #     :param pika.Spec.BasicProperties: Настройки
    #     :param bytes body: Тело сообщения
    #     """
    #     LOGGER.info('Received message # %s from %s: %s',
    #                 basic_deliver.delivery_tag, properties.app_id, body)
    #     self.acknowledge_message(basic_deliver.delivery_tag)
    #
    # def acknowledge_message(self, delivery_tag):
    #     """Подтверждение доств
    #     :param int delivery_tag: The delivery tag from the Basic.Deliver frame
    #     """
    #     LOGGER.info('Acknowledging message %s', delivery_tag)
    #     self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Остановка работы
        """
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        """
        Этот метод вызывается когда RabbitMQ подтверждает
        отмену потребителя. В этот момент мы закроем канал.
        Это вызовет метод on_channel_closed после того как канал будет
        закрыт, что в свою очередь закроет соединение.
        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)
        """
        self._consuming = False
        LOGGER.info(
            'RabbitMQ acknowledged the cancellation of the consumer: %s',
            userdata)
        self.close_channel()

    def close_channel(self):
        """Закрытие канала после отмены потребителя
        """
        LOGGER.info('Closing the channel')
        self._channel.close()

    def run(self,callback,route,queue,exh_type='direct'):
        """Запуск потребителя
        """
        self.EXCHANGE_TYPE = exh_type
        self.callback = callback
        self.QUEUE = queue
        self.ROUTING_KEY = route
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Закрытие соединения
        """
        if not self._closing:
            self._closing = True
            LOGGER.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            LOGGER.info('Stopped')