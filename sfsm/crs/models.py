from django.db import models

# Create your models here.
class host(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.GenericIPAddressField('主机ip')
    inter_ip = models.CharField('外网ip',null=True,max_length=150)
    hostname = models.CharField('主机名', max_length=50)
    port = models.IntegerField('端口',default=22)
    brand = models.CharField('序列号',max_length=50,null=True)
    cpu = models.CharField('cpu',max_length=50,null=True)
    memory = models.CharField('内存大小',max_length=50,null=True)
    system_version = models.CharField('系统版本',max_length=50,null=True)
    label = models.CharField('主机标签',max_length=50,null=True)
    is_active = models.BooleanField('服务器状态',default=False)
    date_joined = models.DateTimeField('创建时间', auto_now_add=True)
    last_login = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return '%s-%s' % (self.ip, self.hostname)

    class Meta:
        verbose_name = '主机管理'
        verbose_name_plural = '主机管理'