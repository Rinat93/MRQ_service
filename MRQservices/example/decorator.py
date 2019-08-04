from MRQservices.decoratos.create_microservice import log,Microservise
from MRQservices.dispatch.service import run
from MRQservices.dispatch.service import Service
# import asyncio
# import asyncore



@Microservise()
async def rests(ctx):
    print(1)
    print(ctx.body)
#
@Microservise(route='api2')
async def asa(ctx):
    print(2)
    print(ctx.body)
    # log.log(body=ctx.body,file='api2.txt')
    # return 'Ну привет друг'

@Microservise(route='api')
async def callback(ctx):
    print(3)
    print(ctx.body)

if __name__ == '__main__':
    run()
# async def run_all():
#     a(name="Хай")
#     asa(name="Хай 2")

# if __name__ == "__main__":
#     server = EchoServer('localhost', 8080)
#     asyncore.loop()