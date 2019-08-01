from MRQservices.decoratos.create_microservice import log,Microservise
# import asyncio
# import asyncore



@Microservise()
def rests(ch, method, properties, body):
    log.log(body=body,file='rests.txt')
    ch.basic_ack(delivery_tag = method.delivery_tag)
#
@Microservise(route='api2')
def asa(ch, method, properties, body):
    log.log(body=body,file='api2.txt')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.basic_consume()
    return 'Ну привет друг'

@Microservise(route='api')
def callback(ch, method, properties, body):
    print(properties)
    log.log(body=body,file='api.txt')
    ch.basic_ack(delivery_tag = method.delivery_tag)

# async def run_all():
#     a(name="Хай")
#     asa(name="Хай 2")

# if __name__ == "__main__":
#     server = EchoServer('localhost', 8080)
#     asyncore.loop()