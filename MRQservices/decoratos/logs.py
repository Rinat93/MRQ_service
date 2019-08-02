import os
import json
'''
    Декоратор для логирования основы сервисов
'''
def loggigs_service(func):

    def writes(*args,**kwargs):
        services = json.loads(args[-1].decode('utf-8'))
        obj = args[0]._registers
        data = [services,obj]
        if not os.path.isdir('log'):
            os.makedirs('log')

        if os.path.isfile(f'log/{obj["SERVICE"]}.json'):
            with open(f'log/{obj["SERVICE"]}.json') as f:
                data.extend(json.load(f))

        with open(f'log/{obj["SERVICE"]}.json','w+') as f:
            # data = json.load(f)
            json.dump(data,f)


        return func(*args,**kwargs)
    return writes