import pymysql
from DBUtils.PooledDB import PooledDB
import crs.config.DB_config as Config
import redis

class Redis(object):
    def __init__(self,ip,password,port=6379):
        try:
            self.pool = redis.ConnectionPool(host=ip, password=password, port=port)
            self.r = redis.Redis(self.pool)
        except Exception as e:
            print('redis连接失败，错误信息%s'%e)

    def str_set(self,k,v,time=None): #time默认失效时间
        self.r.set(k,v,time)

class mysqlConnectionPoll(object):
    def __init__(self,host,user,password,port,dbname):
        self.POOL = PooledDB(creator=pymysql, mincached=Config.DB_MIN_CACHED, maxcached=Config.DB_MAX_CACHED,
                        maxshared=Config.DB_MAX_SHARED,maxconnections=Config.DB_MAX_CONNECYIONS, blocking=Config.DB_BLOCKING,
                        maxusage=Config.DB_MAX_USAGE, setsession=Config.DB_SET_SESSION, charset=Config.DB_CHARSET,
                        host=host,port=port,user=user,passwd=password,db=dbname)
        try:
            self.conn = self.POOL.connection()
        except pymysql.Error as e:
            errormsg = 'Cannot connect to server \n ERRORR(%s):%s' % (e.args[0] , e.args[1])
            print (errormsg)
            exit(2)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    def fetch_all(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def __del__(self):
        self.conn.close()
        self.cursor.close()

