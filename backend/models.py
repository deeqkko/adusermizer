"""
Backend app database models
"""

import uuid
from django.db import models



class Domain(models.Model):
    """Model for domains in control of the app"""
    id = models.CharField("ServerObjectGuid", max_length=50, primary_key=True)
    domain = models.CharField("Domain", max_length=50, unique=True)
    distinguished_name = models.CharField("DistinguishedName", max_length=50, unique=True)
    host_name = models.CharField("HostName", max_length=50)
    ipv4address = models.GenericIPAddressField("IPv4Address", unique=True)
    acc_admin = models.CharField("Account Administrator", max_length=50)
    key_name = models.CharField("Admin Password", max_length=100)

    def __str__(self):
        return self.domain

class DomainGroup(models.Model):
    """Domain security groups"""
    id = models.CharField("ObjectGuid", max_length=50, primary_key=True)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE, null=True)
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=50)
    sam_account_name = models.CharField("SamAccountName",max_length=50)
    group_category = models.CharField("Group Category", max_length=50)
    group_scope = models.CharField("Group Scope", max_length=50)
    display_name = models.CharField("Display Name", max_length=50, null=True)
    distinguished_name = models.CharField("Distinguished Name", max_length=100)
    description = models.TextField("Description", null=True)
    created_by_app = models.BooleanField("Created by app", default=False)

    def __str__(self):
        return self.distinguished_name

class Group(models.Model):
    id = models.UUIDField(
        "UserID",
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField("Name", max_length=50, unique=True)
    sam_account_name = models.CharField("SamAccountName", max_length=50, unique=True)
    group_category = models.IntegerField("GroupCategory")
    group_scope = models.IntegerField("GroupScope")
    display_name = models.CharField("DisplayName", max_length=50, blank=True)
    description = models.CharField("Description", max_length=50, blank=True)
    organizational_unit = models.ForeignKey('OrganizationalUnit', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class DomainOrganizationalUnit(models.Model):
    """Domain Organizational Unit"""
    id = models.CharField("ObjectGuid", max_length=50, primary_key=True)
    ou_id = models.ForeignKey("OrganizationalUnit", on_delete=models.CASCADE, null=True)
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=50)
    distinguished_name = models.CharField("Distinguished Name", max_length=100)
    created_by_app = models.BooleanField("Created by app", default=False)

    def __str__(self):
        return self.distinguished_name

class OrganizationalUnit(models.Model):
    id = models.UUIDField(
        "UserID",
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField("Name", max_length=50)

class DomainUser(models.Model):
    """Model for domain user entities per single app user"""
    id = models.CharField("ObjectGUID", max_length=50, primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    distinguished_name = models.CharField("Distinguished Name", max_length=50)
    user_principal_name = models.CharField(
        "User Principal Name", max_length=50, default=None)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    sam_account_name = models.CharField("SamAccountName", max_length=50)
    created_by_app = models.BooleanField("Created by app", default=False)

    def __str__(self):
        return self.distinguished_name

class User(models.Model):
    """Model for app user"""
    id = models.UUIDField(
        "UserID",
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    sam_account_name = models.CharField(
        "SamAccountName", max_length=50, unique=True)
    given_name = models.CharField("GivenName", max_length=50)
    surname = models.CharField("Surname", max_length=50)
    account_password = models.CharField("Account Password", max_length=50)
    organizational_unit = models.ForeignKey('OrganizationalUnit', null=True, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)
    domains = models.ManyToManyField(Domain, blank=True)

    def __str__(self):
        return self.sam_account_name