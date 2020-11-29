from backend.models import Domain, DomainUser, User
from rest_framework import serializers

class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id','domain', 'host_name','ipv4address','acc_admin','password')

class DomainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainUser
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['domain_users']

# class UserSerializer(serializers.Serializer):
#     id = serializers.UUIDField(read_only=True)
#     sam_account_name = serializers.CharField(required=True, max_length=50)
#     given_name = serializers.CharField(required=False, max_length=50)
#     surname = serializers.CharField(required=False, max_length=50)
#     account_password = serializers.CharField(required=True, max_length=50)
#     domains = serializers.ManyRelatedField(Domain)
#     domain_users = serializers.ManyRelatedField(DomainUser)

