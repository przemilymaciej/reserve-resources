# Generated by Django 4.2.dev20221031113113 on 2022-11-12 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chip',
            fields=[
                ('chip_id', models.AutoField(primary_key=True, serialize=False)),
                ('chip_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'chips',
            },
        ),
        migrations.CreateModel(
            name='PlatformType',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'platform_types',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.TextField(choices=[('REQUESTED', 'Requested'), ('GRANTED', 'Granted'), ('IN_USE', 'In use'), ('COMPLETED', 'Completed'), ('INVALID', 'Invalid'), ('FREE_REQUESTED', 'Free requested')])),
                ('time_requested', models.DateTimeField()),
                ('time_granted', models.DateTimeField(blank=True, null=True)),
                ('time_completed', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'requests',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('network_ip', models.CharField(max_length=255, unique=True)),
                ('power_ip_port', models.CharField(max_length=255)),
                ('console_ip_port', models.CharField(max_length=255)),
                ('is_available', models.BooleanField()),
                ('is_reserved', models.BooleanField()),
                ('rev', models.CharField(max_length=100)),
                ('sku', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('comment', models.TextField(max_length=100)),
                ('workspace', models.CharField(max_length=100)),
                ('chip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources_website.chip')),
                ('platform_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources_website.platformtype')),
                ('request_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources_website.request')),
            ],
            options={
                'db_table': 'resources',
                'ordering': ('description', 'comment'),
            },
        ),
        migrations.CreateModel(
            name='TopologyClass',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'topology_class',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'users',
                'ordering': ('user', 'email', 'full_name'),
            },
        ),
        migrations.CreateModel(
            name='TopologyInstances',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('class_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources_website.topologyclass')),
            ],
            options={
                'db_table': 'topology_instances',
            },
        ),
        migrations.CreateModel(
            name='ResourcesConnections',
            fields=[
                ('topo_node_id', models.AutoField(primary_key=True, serialize=False)),
                ('topo_node_index', models.IntegerField()),
                ('topo_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources_website.topologyinstances')),
                ('topo_node_resource', models.ForeignKey(db_column='resources', on_delete=django.db.models.deletion.CASCADE, to='resources_website.resource')),
            ],
            options={
                'db_table': 'resources_connections',
            },
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='resources_website.user'),
        ),
    ]
