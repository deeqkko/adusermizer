from django.shortcuts import render
from django.shortcuts import HttpResponse
from backend.models import User, Group, Domain
from rest_framework import viewsets
from rest_framework import permissions
from backend.serializers import UserSerializer, GroupSerializer, DomainSerializer

def home(request):
    return HttpResponse(
        "<h1>Adusermizer</h1> \
        <p>A proof-of-concept app for UAS thesis to manage Active Directory users in an environment of multiple independent AD:s wihtout \
            trust relations."
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer