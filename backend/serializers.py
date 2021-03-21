"""Serializer module between views and models. Also token serializer for JWT-tokens."""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from backend.models import Domain, DomainUser, DomainGroup, DomainOrganizationalUnit,\
     User, Group, OrganizationalUnit




class DomainSerializer(serializers.ModelSerializer):
    """Serializer for domain model. All fields included."""
    class Meta:
        model = Domain
        fields = '__all__'

class DomainGroupSerializer(serializers.ModelSerializer):
    """Serializer for domain group model. All fields included."""
    class Meta:
        model = DomainGroup
        fields = '__all__'

class DomainOrganizationalUnitSerializer(serializers.ModelSerializer):
    """Serializer for domain organizational unit model. All fields included."""
    class Meta:
        model = DomainOrganizationalUnit
        fields = '__all__'


class DomainUserSerializer(serializers.ModelSerializer):
    """Serializer for domain user model. All fields included."""
    class Meta:
        model = DomainUser
        fields = '__all__'


class OrganizationalUnitSerializer(serializers.ModelSerializer):
    """Serializer for organizational unit model. All fields included."""
    class Meta:
        model = OrganizationalUnit
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    """Serializer for group model read operations. Includes nested serialization
    from related models"""
    class Meta:
        model = Group
        fields = '__all__'
        depth = 1

class GroupWriteSerializer(serializers.ModelSerializer):
    """Serializer for group models create and update operations."""
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model read operations. Includes nested serialization
    from related models"""
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class UserWriteSerializer(serializers.ModelSerializer):
    """Serializer for user models create and update operations."""
    class Meta:
        model = User
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serialization for obtaining and updating JWT-token"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token
