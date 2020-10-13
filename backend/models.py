from django.db import models
import uuid


class Domain(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    domainName = models.CharField("Fully qualified domain name", max_length=50)
    computerName = models.CharField("Computer name", max_length=50, default="")
    ipaddress = models.GenericIPAddressField("IPv4 address", unique=True, default="")

    def __str__(self):
        return self.domainName

class Group(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    objectSid = models.CharField("Security identifier", max_length=50)
    sAMAccountName = models.CharField("Group name", max_length=20)

    def __str__(self):
        return self.sAMAccountName

class User(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    objectSid = models.CharField("Security identifier", max_length=50)
    userPrincipalName = models.CharField("User logon name", max_length=50)
    givenName = models.CharField("First name", max_length=30, default="")
    sn = models.CharField("Last name", max_length=50, default="")
    domains = models.ManyToManyField(Domain)
    groups = models.ManyToManyField(Group)
    pwdLastSet = models.BooleanField("Force password change on next logon", default=True)

    def __str__(self):
        return self.sn + " " + self.givenName