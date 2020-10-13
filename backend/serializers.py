from backend.models import User, Group, Domain
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url',
            'id', 
            'objectSid',
            'userPrincipalName',
            'givenName',
            'sn',
            'groups',
            'domains',
            'pwdLastSet'
        ]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'objectSid', 'sAMAccountName']

class DomainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Domain
        fields = ['url', 'domainName', 'computerName', 'ipaddress']