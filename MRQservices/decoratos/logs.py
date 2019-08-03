import os
import json
'''
    Декоратор для логирования основы сервисов
'''
async def loggigs_service(func):

    async def writes(ctx):
        services = json.loads(ctx.body.decode('utf-8'))
        obj = services._registers
        data = [services,obj]
        if not os.path.isdir('log'):
            os.makedirs('log')

        if os.path.isfile(f'log/{obj["SERVICE"]}.json'):
            with open(f'log/{obj["SERVICE"]}.json') as f:
                data.extend(json.load(f))

        with open(f'log/{obj["SERVICE"]}.json','w+') as f:
            # data = json.load(f)
            json.dump(data,f)


        await func(ctx)
    return writes