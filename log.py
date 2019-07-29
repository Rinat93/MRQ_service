import os
def log(*args,**kwargs):
    file = 'logs.log'
    if 'file' in kwargs:
        file = kwargs['file']
    with open(file,'w+') as f:
        reads = ''
        if os.path.isfile(file):
            reads = f.read()
        logs = str(kwargs['body'])
        f.write(logs)
