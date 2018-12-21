from rest_framework import viewsets, serializers, generics, filters,mixins
from django_filters.rest_framework import DjangoFilterBackend
from crs.serializers import *
from .renderers import APIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from copy import deepcopy
from crs.common.views import Redis
from django.http import JsonResponse
from crs.models import *
import redis,json



# Create your views here.
@api_view(['GET'])
@renderer_classes((APIRenderer,))
def userinfo(request):
    return Response({
        'roles': ['admin'] if request.user.is_superuser else ['user'],
        'token': ['admin'] if request.user.is_superuser else ['user'],
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': request.user.username
    })


class userAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data['password']
        groups = serializer.data['groups']
        user_permissions = serializer.data['user_permissions']
        newData = deepcopy(serializer.data)
        newData.pop('groups')
        newData.pop('user_permissions')
        user = User.objects.create(**newData)
        user.set_password(password)
        # print(groups, user_permissions)
        [user.groups.add(x) for x in groups]
        [user.user_permissions.add(x) for x in user_permissions]
        # map(lambda x: user.groups.add(x), groups)
        # map(lambda x: user.user_permissions.add(x), user_permissions)
        user.save()
        return Response('ok')


class GroupAPI(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionAPI(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class HostAPI(viewsets.ModelViewSet):
    queryset = host.objects.all()
    serializer_class = HostSercializer
    filter_backends = [DjangoFilterBackend]


#查询功能
class HostList(generics.ListAPIView):
    queryset = host.objects.all()
    serializer_class = HostSercializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('hostname','ip')

class RedisHostApi(viewsets.ModelViewSet):
    pool = redis.ConnectionPool(host='192.168.0.79',pool=7777,db=0)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline()

    @renderer_classes((APIRenderer,))
    def list(self, request, *args, **kwargs):
        key_list = []
        keys = self.r.keys()
        for key in keys:
            key_list.append(key)
            self.pipe.get(key)
        base_data = {}
        for (k, v) in zip(key_list, self.pipe.execute()):
            base_data[k] = json.loads(v)['collect']
        return base_data
    # def create(self, request, *args, **kwargs):
    #     pass
    # def update(self, request, *args, **kwargs):
    #     pass
    # def retrieve(self, request, *args, **kwargs):
    #     pass
    # def destroy(self, request, *args, **kwargs):
    #     pass

# def serverlist(request):
#     jmsconn = mysqlConnectionPoll('192.168.1.213', 'shiyiwen', 'abc123456', 3306, 'jumpserver')
#     if request.method == 'GET':
#         serverlistsql = 'select * from jasset_asset'
#         res = jmsconn.fetch_all(serverlistsql)
#         for i in res:
#             host.objects.create(
#                 id=i['id'], ip=i['ip'], hostname=i['hostname'], port=i['port'], brand=i['brand'], cpu=i['cpu'],
#                 memory=i['memory'], system_version=i['system_version'], is_active=i['is_active']
#             )
#         return JsonResponse(i)
#     elif request.method == 'PUT':
#         pass
#     else:
#         return Response({
#             'msg': 'Error'
#         })
