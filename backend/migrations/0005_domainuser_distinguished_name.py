# Generated by Django 3.1.2 on 2020-11-06 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20201105_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainuser',
            name='distinguished_name',
            field=models.CharField(default='', max_length=50, verbose_name='Distinguished Name'),
            preserve_default=False,
        ),
    ]
