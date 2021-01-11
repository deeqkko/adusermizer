# Generated by Django 3.1.2 on 2021-01-08 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_auto_20210107_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organizational_units',
        ),
        migrations.AddField(
            model_name='user',
            name='organizational_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.organizationalunit'),
        ),
    ]
