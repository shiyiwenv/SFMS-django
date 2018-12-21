from django.conf.urls import url,include
from rest_framework import routers
from crs.views import *
router = routers.DefaultRouter()
router.register(r'users', userAPI)
router.register(r'groups', GroupAPI)
router.register(r'Permission', PermissionAPI)
router.register(r'host',HostAPI)
router.register(r'rhost',RedisHostApi,base_name='ok')



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/user/info', userinfo),
    url(r'^hostlist', HostList.as_view())
    # url(r'^api/host/jumpserver',serverlist)
]