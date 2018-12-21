from rest_framework import serializers
from crs import models
from django.contrib.auth.models import Group, User, Permission


class FormatTimeField(serializers.BaseSerializer):
    def to_representation(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('__all__')


class GroupSerializer(serializers.ModelSerializer):
    # permissions = serializers.ReadOnlyField(required=False,source='Permission.codename',allow_null=True
    #                                         , read_only=True)
    class Meta:
        model = Group
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    last_login = FormatTimeField(read_only=True)
    date_joined = FormatTimeField(read_only=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    # user_permissions = PermissionSerializer()

    class Meta:
        model = User
        fields = ('__all__')

class HostSercializer(serializers.ModelSerializer):
    last_login = FormatTimeField(read_only=True)
    date_joined = FormatTimeField(read_only=True)

    class Meta:
        model = models.host
        fields = ('__all__')