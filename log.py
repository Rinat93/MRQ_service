def log(file='logs.log',*args,**kwargs):
    with open(file,'w+') as f:
        reads = f.read()
        f.write(str(*args, **kwargs)+reads)
