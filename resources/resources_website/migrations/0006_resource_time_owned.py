# Generated by Django 4.2.dev20221031113113 on 2022-12-28 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources_website', '0005_resource_last_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='time_owned',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]