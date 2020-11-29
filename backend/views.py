"""
Backend app api views
"""
from rest_framework import viewsets
from rest_framework.response import Response
from backend.models import Domain, User, DomainUser
from backend.serializers import DomainSerializer, UserSerializer, DomainUserSerializer
from .services import connect, connect_domain, get_users, create_user, delete_user

keys = {'sam_account_name', 'user_principal_name',
        'given_name', 'surname', 'account_password'}


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def create(self, request):
        req = request.data
        conn = connect(req.get('ipv4address'), req.get(
            'acc_admin'), req.get('password'))
        server_props = connect_domain(conn)
        data = {'id': server_props.get("ServerObjectGuid")}
        data.update(req)
        domainserializer = DomainSerializer(data=data)
        if domainserializer.is_valid():
            domainserializer.save()
        return Response(data)


keys = {'sam_account_name', 'user_principal_name',
        'given_name', 'surname', 'account_password'}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        req = request.data
        domains = Domain.objects.filter(id__in=req.get('domains'))
        
        userserializer = UserSerializer(data=req)
        if userserializer.is_valid():
            userserializer.save()

        req.pop('domains')
        user = User.objects.get(sam_account_name=req['sam_account_name'])
        for domain_controller in domains:
            conn = connect(domain_controller.ipv4address,
                domain_controller.acc_admin,
                domain_controller.password)
            domain_user = get_users(conn, req.get('sam_account_name'))
            user_principal_name = user.sam_account_name + "@" + domain_controller.domain 
            req.update({'user_principal_name': user_principal_name})
            
            if 'SamAccountName' not in domain_user.keys():
                domain_user = create_user(conn, req)
            # Laita ehtolause kuntoon tapauksessa, että käyttäjä on jo luotu domainiin
            domain_user.update({'user_id': user.id, 'domain': domain_controller.id})
            print(domain_user)    
            domain_controllerserializer = DomainUserSerializer(data=domain_user)
            if domain_controllerserializer.is_valid():
                domain_controllerserializer.save()

        return Response({'status': 'user created'})

    def partial_update(self, request, pk=None):
        req = self.request.data
        all_domains = Domain.objects.all()
        new_domains = Domain.objects.filter(id__in=req['domains'])
        delete_domains = Domain.objects.exclude(id__in=req['domains'])
        user = self.get_object()

        for domain_controller in all_domains:
            conn = connect(domain_controller.ipv4address, domain_controller.acc_admin, domain_controller.password)
            domain_user = get_users(conn, user.sam_account_name)
            if domain_controller in new_domains and 'SamAccountName' not in domain_user.keys():

                domain_controller_user_attr = {key: value for key,value in user.__dict__.items() if key in keys}
                user_principal_name = user.sam_account_name + "@" + domain_controller.domain
                domain_controller_user_attr.update(
                    {'user_principal_name': user_principal_name})
                create_user(conn, domain_controller_user_attr)

                domain_user = get_users(conn, user.sam_account_name)
                domain_user = {'id': domain_user['ObjectGUID'],
                               'user_id': user.id,
                               'distinguished_name': domain_user['DistinguishedName'],
                               'user_principal_name': user_principal_name,
                               'domain': domain_controller.id,
                               'sam_account_name': domain_user['SamAccountName']}
                domain_controllerserializer = DomainUserSerializer(data=domain_user)
                if domain_controllerserializer.is_valid():
                    domain_controllerserializer.save()

            if domain_controller in delete_domains and 'SamAccountName' in domain_user.keys():
                delete_user(conn, user.sam_account_name)
                DomainUser.objects.filter(sam_account_name=user.sam_account_name).get(
                    domain__id=domain_controller.id).delete()

        userserializer = UserSerializer(user, data=req, partial=True)
        if userserializer.is_valid():
            userserializer.update(user, userserializer.validated_data)

        return Response({'status': req['domains']})

    def destroy(self, request, pk=None):
        """
        Laita varmistuksia!
        """
        user = self.get_object()
        for domain_controller in Domain.objects.filter(user__sam_account_name=user.sam_account_name):
            conn = connect(domain_controller.ipv4address, domain_controller.acc_admin, domain_controller.password)
            delete_user(conn, user.sam_account_name)

        user.delete()

        return Response({'status': 'User deleted'})
