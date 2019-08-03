import aio_pika
import json
class Base(object):
    EXCHANGE = 'message'
    EXCHANGE_TYPE = 'topic'
    QUEUE = 'text'
    ROUTING_KEY = 'example.text'
    RABBITMQ = "amqp://guest:guest@127.0.0.1/"

    async def connect(self,loop=None):
        connection = await aio_pika.connect_robust(
            self.RABBITMQ,
            loop=loop
        )
        return connection

    # Настройка канала
    async def channel_settings(self,client):
        channel = await client.channel()
        src_exchange = await channel.declare_exchange(
            self.EXCHANGE_TYPE, auto_delete=True
        )
        queue = await channel.declare_queue(self.QUEUE,auto_delete=True)

        await queue.bind(src_exchange, self.ROUTING_KEY)
        return (queue,src_exchange)


    # Запускаем слушателя
    async def run_consumer(self,callback,loop=None):
        connection = await self.connect(loop)
        async with connection:
            # Creating channel
            queue,channel = await self.channel_settings(connection)

            # Declaring queue
            # queue = await channel.declare_queue(
            #     self.QUEUE, auto_delete=True,durable=True
            # )
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await callback(message)
                        if queue.name in message.body.decode():
                            break
    # Публикатор
    async def run_publisher(self,body,loop=None):
        connection = await self.connect(loop)
        async with connection:
            # Creating channel
            queue, channel = await self.channel_settings(connection)
            if type(body) == dict:
                body = json.dumps(body, ensure_ascii=False).encode()
            else:
                body = body.encode()
            print(body)
            await channel.publish(
                aio_pika.Message(
                    body=body,
                    content_type = 'json'
                ),
                routing_key = self.ROUTING_KEY,
            )