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



@Microservise
async def a(*args,**kwargs):
    print(1)
    log.log(**kwargs)

@Microservise(route='api')
async def asa(*args,**kwargs):
    print(0)
    log.log(**kwargs)

# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     print(ch)
#     print(method)
#     print(properties)
#     ch.basic_ack(delivery_tag = method.delivery_tag)

async def run_all():
    a(name="Хай")
    asa(name="Хай 2")

if __name__ == "__main__":
    print(a())
    # server = EchoServer('localhost', 8080)
    # asyncore.loop()
    # asyncio.run(run_all())
    # asyncio.run(Servers.RunGateway())
    # asyncio.run(a(name="Хай"))
    # asyncio.run(asa(name="Хай 2"))
    ## MicroRq('localhost').create_channels('task_queue',callback)
    #MicroRq('localhost').subscribe('logs',callback,routing_key=['users.*','admin.*'],exchange_type='topic')