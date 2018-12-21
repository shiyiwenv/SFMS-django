import consul
import json

class Consulclient():
    def __init__(self,host=None, port=None, token=None, scheme='http'):
        self.host = host
        self.port = port
        self.token = token
        self.consul = consul.Consul(host=host, port=port, token=token, scheme=scheme)

    def get_kv(self, Key_name):
        index = None
        index, data = consul.kv.get(Key_name, index=index)
        return json.loads(data['Value'])


c = consul.Consul(host='192.168.0.64',port=8500,scheme='http')
index = None
index,data = c.kv.get('sfms/dev/redis/config/connections', index=index,)
redisconf = json.loads(data['Value'])
servers = redisconf['servers']
print(servers)