from backend.models import Domain
from backend.serializers import DomainSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .services import connect, connect_domain

@api_view(['GET', 'POST'])
def domain_list(request, format=None):
    """
    List all domains or create a new domain
    """
    if request.method == 'GET':
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        req = request.data
        conn = connect(req.get('ipv4address'), req.get('acc_admin'), req.get('password'))
        server_props = connect_domain(conn)
        data = {
            'id':server_props.get("ServerObjectGuid"), 
            'domain':server_props.get("Domain"),
            'host_name':server_props.get("HostName") 
            }
        print(data)
        data.update(request.data)
        serializer = DomainSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def domain_detail(request, pk, format=None):
    """
    Retrieve, update or delete a domain
    """
    try:
        domain = Domain.objects.get(pk=pk)
    except Domain.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DomainSerializer(domain, many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        domain.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
