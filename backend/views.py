"""
Backend app api views
"""
from rest_framework import viewsets
from rest_framework.response import Response
from backend.models import Domain, User, DomainUser, DomainGroup, DomainOrganizationalUnit,\
     Group, OrganizationalUnit
from backend.serializers import DomainSerializer, UserSerializer, DomainUserSerializer,\
     DomainGroupSerializer, DomainOrganizationalUnitSerializer, OrganizationalUnitSerializer,\
     GroupSerializer
from .services import connect, connect_domain, remove_domain, get_user, get_users, \
     get_groups, create_group, delete_group, create_user, delete_user, \
     get_organizational_units, create_organizational_unit, delete_organizational_unit

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
        data = {
            'id': server_props.get("ServerObjectGuid"),
            'distinguished_name': server_props.get("DefaultPartition")
            }
        data.update(req)
        domainserializer = DomainSerializer(data=data)
        if domainserializer.is_valid():
            domainserializer.save()

        domain_groups = get_groups(conn)
        for group in domain_groups:
            group.update({'domain':data['id']})
            domaingroupserializer = DomainGroupSerializer(data=group)
            if domaingroupserializer.is_valid():
                domaingroupserializer.save()

        domain_ous = get_organizational_units(conn)
        for ou in domain_ous:
            ou.update({'domain':data['id']})
            domain_ouserializer = DomainOrganizationalUnitSerializer(data=ou)
            if domain_ouserializer.is_valid():
                domain_ouserializer.save()

        domain_users = get_users(conn)
        for domain_user in domain_users:
            domain_user.update({'domain':data['id']})
            domain_user_serializer = DomainUserSerializer(data=domain_user)
            if domain_user_serializer.is_valid():
                domain_user_serializer.save()
        

        return Response(data)

    def destroy(self, request, pk=None):
        domain = self.get_object()
        domain_users = DomainUser.objects.filter(domain__id=domain.id)
        domain_groups = DomainGroup.objects.filter(domain__id=domain.id)
        domain_ous = DomainOrganizationalUnit.objects.filter(domain__id=domain.id)
        conn = connect(domain.ipv4address, domain.acc_admin, domain.password)

        for domain_user in domain_users:
            if domain_user.created_by_app:
                delete_user(conn, domain_user.sam_account_name)
            domain_user.delete()

        for domain_group in domain_groups:
            if domain_group.created_by_app:
                deleted_group = deleted_group(conn, domain_group.id)
            domain_group.delete()
        
        for domain_ou in domain_ous:
            if domain_ou.created_by_app:
                delete_organizational_unit(conn, domain_ou.id)
            domain_ou.delete()
        
        remove_domain(conn)
        domain.delete()
        return Response({'status':'Domain removed'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        req = self.request.data
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
            domain_user = get_user(conn, req.get('sam_account_name'))
            user_principal_name = user.sam_account_name + "@" + domain_controller.domain
            req.update({'user_principal_name': user_principal_name})
            req.update({'created_by_app': True})
            

            if 'sam_account_name' not in domain_user.keys():
                domain_user = create_user(conn, req)
            # Laita ehtolause kuntoon tapauksessa, että käyttäjä on jo luotu domainiin
            domain_user.update(
                {'user_id': user.id, 'domain': domain_controller.id})
            print(domain_user)
            domain_controllerserializer = DomainUserSerializer(
                data=domain_user)
            if domain_controllerserializer.is_valid():
                domain_controllerserializer.save()

        return Response({'status': 'user created'})

    def partial_update(self, request, pk=None):
        keys = {'sam_account_name', 'user_principal_name',
        'given_name', 'surname', 'account_password'}
        req = self.request.data
        all_domains = Domain.objects.all()
        new_domains = Domain.objects.filter(id__in=req['domains'])
        delete_domains = Domain.objects.exclude(id__in=req['domains'])
        user = self.get_object()
        print('delete domains', delete_domains)

        for domain_controller in all_domains:
            conn = connect(domain_controller.ipv4address,
                           domain_controller.acc_admin, domain_controller.password)
            domain_user = get_user(conn, user.sam_account_name)

            if domain_controller in new_domains and 'SamAccountName' not in domain_user.keys():

                domain_controller_user_attr = {
                    key: value for key, value in user.__dict__.items() if key in keys}
                user_principal_name = user.sam_account_name + "@" + domain_controller.domain
                domain_controller_user_attr.update(
                    {'user_principal_name': user_principal_name})
                create_user(conn, domain_controller_user_attr)

                domain_user = get_user(conn, user.sam_account_name)
                domain_user = {'id': domain_user['id'],
                               'user_id': user.id,
                               'distinguished_name': domain_user['distinguished_name'],
                               'user_principal_name': user_principal_name,
                               'domain': domain_controller.id,
                               'sam_account_name': domain_user['sam_account_name']}
                domain_controllerserializer = DomainUserSerializer(
                    data=domain_user)
                if domain_controllerserializer.is_valid():
                    domain_controllerserializer.save()

            if domain_controller in delete_domains and 'sam_account_name' in domain_user.keys():
                delete_user(conn, user.sam_account_name)
                delete_domain = DomainUser.objects.filter(sam_account_name=user.sam_account_name).get(
                    domain__id=domain_controller.id)
                print(delete_domain)
                delete_domain.delete()

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
            conn = connect(domain_controller.ipv4address,
                           domain_controller.acc_admin, domain_controller.password)
            delete_user(conn, user.sam_account_name)

        user.delete()

        return Response({'status': 'User deleted'})

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        req = request.data
        update_domain_group = []
        
        for domain in Domain.objects.all():
            conn = connect(domain.ipv4address,domain.acc_admin,domain.password)
            domain_groups = DomainGroup.objects.filter(domain__domain=domain.domain).filter(name=req['name'])
            if not domain_groups:
                req.update({'distinguished_name':domain.distinguished_name})
                new_domain_group = create_group(conn, req)
                new_domain_group.update({
                    'domain':domain.id,
                    'created_by_app': True
                    })
                print(new_domain_group)
                domain_group_serializer = DomainGroupSerializer(data=new_domain_group)
                if domain_group_serializer.is_valid():
                    domain_group_serializer.save()
                    update_domain_group.append(new_domain_group['id'])
                print(domain_group_serializer.errors)

        req.update({
            'domain_groups':update_domain_group,
            'created_by_app': True
            })
        group_serializer = GroupSerializer(data=req)
        if group_serializer.is_valid():
            group_serializer.save()
        print(group_serializer.errors)

        return Response({'status':'group created'})

    def destroy(self, request, pk=None):
        group = self.get_object()
        domains = Domain.objects.all()
        result = []

        for domain in domains:
            domain_group = DomainGroup.objects.filter(domain__id=domain.id).get(name=group.name)
            conn = connect(domain.ipv4address, domain.acc_admin, domain.password)
            result.append(delete_group(conn, domain_group.distinguished_name))
            domain_group.delete()

        group.delete()

        return Response({'status': result})
        
class OrganizationalUnitViewSet(viewsets.ModelViewSet):
    queryset = OrganizationalUnit.objects.all()
    serializer_class = OrganizationalUnitSerializer

class DomainUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DomainUser.objects.all()
    serializer_class = DomainUserSerializer

class DomainGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DomainGroup.objects.all()
    serializer_class = DomainGroupSerializer

class DomainOrganizationalUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DomainOrganizationalUnit.objects.all()
    serializer_class = DomainOrganizationalUnitSerializer