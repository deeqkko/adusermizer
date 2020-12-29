# Generated by Django 3.1.2 on 2020-12-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20201215_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationalunit',
            name='domain_ous',
            field=models.ManyToManyField(to='backend.DomainOrganizationalUnit'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='backend.Group'),
        ),
    ]