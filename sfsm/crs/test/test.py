import  redis,json
pool = redis.ConnectionPool(host='192.168.0.79',port=7777,db=0)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline()
key_list = []
keys = r.keys()
for key in keys:
    key_list.append(key)
    pipe.get(key)
base_data = {}
for (k,v) in zip(key_list, pipe.execute()):
    base_data[k] = json.loads(v)['collect']
print(base_data)
