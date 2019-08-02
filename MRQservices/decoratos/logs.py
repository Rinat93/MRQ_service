import os
import json
'''
    Декоратор для логирования основы сервисов
'''
def loggigs_service(func):

    def writes(*args,**kwargs):
        services = json.loads(args[-1].decode('utf-8'))
        data = [kwargs]
        data.append(services)
        if not os.path.isdir('log'):
            os.makedirs('log')

        if os.path.isfile(f'log/{services["SERVICE"]}'):
            with open(f'log/{services["SERVICE"]}.json') as f:
                data.extend(json.load(f))

        with open(f'log/{services["SERVICE"]}.json','w+') as f:
            # data = json.load(f)
            json.dump(services,f)
        return func(*args,**kwargs)
    return writes