from django.contrib.auth.models import User as DjangoUser
from backend.models import Domain, DomainUser, DomainGroup, DomainOrganizationalUnit,\
     User, Group, OrganizationalUnit
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class DomainGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainGroup
        fields = '__all__'

class DomainOrganizationalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainOrganizationalUnit
        fields = '__all__'


class DomainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainUser
        fields = '__all__'


class OrganizationalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationalUnit
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        depth = 1

class GroupWriteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Group
            fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username

        return token