"""
Backend app database models
"""

import uuid
from django.db import models



class Domain(models.Model):
    """Model for domains in control of the app"""
    id = models.CharField("ServerObjectGuid", max_length=50, primary_key=True)
    domain = models.CharField("Domain", max_length=50, unique=True)
    host_name = models.CharField("HostName", max_length=50)
    ipv4address = models.GenericIPAddressField("IPv4Address", unique=True)
    acc_admin = models.CharField("Account Administrator", max_length=50)
    password = models.CharField("Admin Password", max_length=100)

    def __str__(self):
        return self.domain


class DomainUser(models.Model):
    """Model for domain user entities per single app user"""
    id = models.CharField("ObjectGUID", max_length=50, primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, default="")
    distinguished_name = models.CharField("Distinguished Name", max_length=50)
    user_principal_name = models.CharField(
        "User Principal Name", max_length=50, default=None)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    sam_account_name = models.CharField("SamAccountName", max_length=50)

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
    domains = models.ManyToManyField(Domain)
    domain_users = models.ManyToManyField(DomainUser, blank=True)

    def __str__(self):
        return self.sam_account_name
