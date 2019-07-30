from decoratos.create_microservice import log,Microservise
import asyncio
import asyncore

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = EchoHandler(sock)



@Microservise()
def rests(ch, method, properties, body):
    print(1)
    log.log(body=body,file='rests.txt')
    ch.basic_ack(delivery_tag = method.delivery_tag)
#
@Microservise(route='api2')
def asa(ch, method, properties, body):
    print(0)
    log.log(body=body,file='api2.txt')
    ch.basic_ack(delivery_tag=method.delivery_tag)

@Microservise(route='api')
def callback(ch, method, properties, body):
    print(properties)
    log.log(body=body,file='api.txt')
    ch.basic_ack(delivery_tag = method.delivery_tag)

# async def run_all():
#     a(name="Хай")
#     asa(name="Хай 2")

if __name__ == "__main__":
    server = EchoServer('localhost', 8080)
    asyncore.loop()