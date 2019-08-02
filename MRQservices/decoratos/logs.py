import os
import json
def loggigs_service(func):

    def writes(*args,**kwargs):
        if os.path.isdir('log'):
            data = [kwargs]
            data.extend(args)
            if os.path.isfile(f'log/{services}'):
                with open(f'log/{services}.json') as f:
                    data.extend(json.load(f))

            with open(f'log/{services}.json','w+') as f:
                # data = json.load(f)
                json.dump(data,f)
        else:
            print("Нет папки log")
        return func(*args,**kwargs)