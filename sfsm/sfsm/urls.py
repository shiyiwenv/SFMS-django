from django.contrib import admin
from django.conf.urls import url,include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url('admin/', admin.site.urls),
    url('^', include('crs.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
]
