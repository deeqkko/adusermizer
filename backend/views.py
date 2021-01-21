"""
Backend app api views
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from backend.models import Domain, User, DomainUser, DomainGroup, DomainOrganizationalUnit,\
     Group, OrganizationalUnit
from backend.serializers import DomainSerializer, UserSerializer, DomainUserSerializer,\
     DomainGroupSerializer, DomainOrganizationalUnitSerializer, OrganizationalUnitSerializer,\
     GroupSerializer, MyTokenObtainPairSerializer
from .services import connect, connect_domain, remove_domain, get_user, get_users, \
     get_groups, create_group, move_group, delete_group, create_user, delete_user, \
     get_organizational_units, create_organizational_unit, delete_organizational_unit, \
     add_group_member, remove_group_member, move_object_to_ou

########################################################################################
#                                                                                      #
#                                     Domain Viewset                                   #
#                                                                                      #
########################################################################################


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        req = request.data
        conn = connect(req['ipv4address'], req['acc_admin'], req['key_name'])
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
        conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)

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

########################################################################################
#                                                                                      #
#                                     User Viewset                                     #
#                                                                                      #
########################################################################################


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        domains = Domain.objects.all()
        new_user = self.request.data 
        new_user.update({'domains':list(domains.values_list("id", flat=True))})
        new_user_serializer = UserSerializer(data=new_user)
        if new_user_serializer.is_valid():
            new_user_serializer.save()
            #domains = Domain.objects.filter(id__in=new_user['domains'])
            domains = Domain.objects.all()
            for domain in domains:
                conn = connect(domain.ipv4address,domain.acc_admin,domain.key_name)
                result = create_user(conn, new_user)
                result.update({
                    'user_id': User.objects.get(sam_account_name=new_user['sam_account_name']).id,
                    'domain': domain.id,
                    'created_by_app':True
                    })
                new_domain_user_serializer = DomainUserSerializer(data=result)
                if new_domain_user_serializer.is_valid():
                    new_domain_user_serializer.save()
                print(new_domain_user_serializer.errors)

        print(new_user_serializer.errors)

        return Response(new_user_serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_group(self, request, pk=None):
        user = self.get_object()
        domain_users = DomainUser.objects.filter(user_id=user.id)
        new_groups = Group.objects.filter(id__in=request.data['groups'])
        domain_groups = DomainGroup.objects.filter(group_id__in=new_groups.values_list('id', flat=True))
        domains = Domain.objects.filter(id__in=domain_groups.values_list('domain', flat=True))
        response = []
        user_and_group = {}

        for domain in domains:
            conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)
            for domain_group in domain_groups.filter(domain__id=domain.id):
                user_and_group = {}
                user_and_group.update({
                    'group':domain_group.id,
                    'user':domain_users.get(domain__id=domain.id).id
                })
                response.append(add_group_member(conn, user_and_group))

        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        print(user_serializer.errors)

        return Response(user_serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_from_group(self, request, pk=None):
        user = self.get_object()
        domain_users = DomainUser.objects.filter(user_id=user.id)
        new_groups = Group.objects.filter(id__in=request.data['groups'])
        domain_groups = DomainGroup.objects.filter(id__in=new_groups.values_list('domain_groups', flat=True))
        domains = Domain.objects.filter(id__in=domain_groups.values_list('domain', flat=True))
        response = []
        user_and_group = {}

        for domain in domains:
            conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)
            for domain_group in domain_groups.filter(domain__id=domain.id):
                user_and_group = {}
                user_and_group.update({
                    'group':domain_group.id,
                    'user':domain_users.get(domain__id=domain.id).id
                })
                response.append(remove_group_member(conn, user_and_group))
        
        groups_to_delete = request.data['groups']
        for group_to_delete in groups_to_delete:
            user.groups.remove(group_to_delete)


        return Response(request.data)

    @action(detail=True, methods=['post'])
    def add_to_ou(self, request, pk=None):
        user = self.get_object()
        domain_users = DomainUser.objects.filter(user_id=user.id)
        organizational_unit = OrganizationalUnit.objects.filter(id__contains=request.data['organizational_unit'])
        domain_ous = DomainOrganizationalUnit.objects.filter(ou_id__in=organizational_unit.values_list('id', flat=True))
        domains = Domain.objects.filter(id__in=domain_users.values_list('domain', flat=True))

        for domain in domains:
            conn = connect(domain.ipv4address, domain.acc_admin,domain.key_name)
            for domain_ou in domain_ous.filter(domain__id=domain.id):
                domain_user = domain_users.get(domain=domain.id)
                properties = {
                    'identity': domain_user.id,
                    'targetpath': domain_ou.distinguished_name
                }
                result = move_object_to_ou(conn, properties)
                print(result)
                domain_user_serializer = DomainUserSerializer(domain_user, data=result, partial=True)
                if domain_user_serializer.is_valid():
                    domain_user_serializer.save()
                print(domain_user_serializer.errors)
        
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        print(user_serializer.errors)

        return Response(user_serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def reset_key_name(self, request, pk=None):
        self.get_object()
        return Response('Coming soon...')


    def destroy(self, request, pk=None):
        user = self.get_object()
        domain_users = DomainUser.objects.filter(user_id__id=user.id)
        response = []
        
        for domain in user.domains.all(): 
            conn = connect(domain.ipv4address,domain.acc_admin,domain.key_name)
            domain_user = domain_users.get(domain__id=domain.id)
            domain_user_dict = DomainUserSerializer(domain_user).data
            domain_user_dict.pop('user_id', None)
            print(domain_user_dict)
            response.append(delete_user(conn, domain_user_dict)) #requestissa jotain vikaa?

        user.delete()

        return Response(response)

########################################################################################
#                                                                                      #
#                                     Group Viewset                                    #
#                                                                                      #
########################################################################################

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        new_group = request.data
        new_group_serializer = GroupSerializer(data=new_group)
        if new_group_serializer.is_valid():
            new_group_serializer.save()
            domains = Domain.objects.all()
            for domain in domains:
                conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)
                new_group.update({'distinguished_name':domain.distinguished_name})
                result = create_group(conn, new_group)
                result.update({
                    'group_id': Group.objects.get(sam_account_name=new_group['sam_account_name']).id,
                    'domain': domain.id,
                    'created_by_app': True
                })
                print(result)
                domain_group_serializer = DomainGroupSerializer(data=result)
                if domain_group_serializer.is_valid():
                    domain_group_serializer.save()
                print(domain_group_serializer.errors)
            
        return Response(new_group_serializer.data)

 

    @action(detail=True, methods=['post'])
    def add_to_ou(self, request, pk=None):
        new_ou = request.data
        group = self.get_object()
        domain_groups = DomainGroup.objects.filter(group_id=group.id)
        organizational_unit = OrganizationalUnit.objects.get(id=new_ou['organizational_unit'])
        domain_ous = DomainOrganizationalUnit.objects.filter(ou_id=organizational_unit.id)
        domains = Domain.objects.all()
        print(organizational_unit, domain_ous, domains)

        for domain in domains:
            conn = connect(domain.ipv4address, domain.acc_admin,domain.key_name)
            for domain_ou in domain_ous.filter(domain__id=domain.id):
                domain_group = domain_groups.get(domain=domain.id)
                properties = {
                    'identity': domain_group.id,
                    'targetpath': domain_ou.distinguished_name
                }
                result = move_object_to_ou(conn, properties)
                print(result)
                domain_group_serializer = DomainGroupSerializer(domain_group, data=result, partial=True)
                if domain_group_serializer.is_valid():
                    domain_group_serializer.save()
                print(domain_group_serializer.errors)
        
        group_serializer = GroupSerializer(group, data=request.data, partial=True)
        if group_serializer.is_valid():
            group_serializer.save()
        print(group_serializer.errors)

        return Response(group_serializer.data)


    def destroy(self, request, pk=None):
        group = self.get_object()
        domains = Domain.objects.all()
        result = []

        for domain in domains:
            domain_group = DomainGroup.objects.filter(domain__id=domain.id).get(name=group.name)
            conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)
            result.append(delete_group(conn, domain_group.distinguished_name))
            domain_group.delete()

        group.delete()

        return Response({'status': result})

########################################################################################
#                                                                                      #
#                                Organizational Unit Viewset                           #
#                                                                                      #
########################################################################################
        
class OrganizationalUnitViewSet(viewsets.ModelViewSet):
    queryset = OrganizationalUnit.objects.all()
    serializer_class = OrganizationalUnitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        req = request.data

        ou_serializer = OrganizationalUnitSerializer(data=req)
        if ou_serializer.is_valid():
            ou_serializer.save()
            for domain in Domain.objects.all():
                conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)
                req.update({'path':domain.distinguished_name})
                new_domain_ou = create_organizational_unit(conn, req)
                new_domain_ou.update({
                    'ou_id': OrganizationalUnit.objects.get(name=req['name']).id,
                    'domain':domain.id,
                    'created_by_app': True
                })
                print(new_domain_ou)
                domain_ou_serializer = DomainOrganizationalUnitSerializer(data=new_domain_ou)
                if domain_ou_serializer.is_valid():
                    domain_ou_serializer.save()
                print(domain_ou_serializer.errors) 
    
        return Response(ou_serializer.data)



    def destroy(self, request, pk=None):
        ou = self.get_object()
        domains = Domain.objects.all()
        result = []

        for domain in domains:
            conn = connect(domain.ipv4address, domain.acc_admin, domain.key_name)
            domain_ou = DomainOrganizationalUnit.objects.filter(ou_id=ou.id).get(domain=domain.id)
            sub_ous = DomainOrganizationalUnit.objects.filter(distinguished_name__contains=domain_ou.distinguished_name).exclude(name=domain_ou.name)
            sub_groups = DomainGroup.objects.filter(distinguished_name__contains=domain_ou.distinguished_name)
            sub_users = DomainUser.objects.filter(distinguished_name__contains=domain_ou.distinguished_name)
            if sub_ous or sub_groups or sub_users:
                return Response("Cannot delete. Leaf objects detected.")

            result.append(delete_organizational_unit(conn, domain_ou.distinguished_name))
            domain_ou.delete()
        
        ou.delete()

        return Response({'status':result})

class DomainUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DomainUser.objects.all()
    serializer_class = DomainUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class DomainGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DomainGroup.objects.all()
    serializer_class = DomainGroupSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class DomainOrganizationalUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DomainOrganizationalUnit.objects.all()
    serializer_class = DomainOrganizationalUnitSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer