from django.db import models
from datetime import datetime, timedelta
from django.db import connection
from django.conf import settings

# get a way to log the errors:
import logging
log = logging.getLogger(__name__)

#BASE_IP = "10.100.1." # old method
SINGLE_TOPO_CLASS_ID = 1


class User(models.Model):
    user = models.CharField(primary_key=True, max_length=255)
    email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'
        ordering = ('user', 'email', 'full_name')

    def __str__(self):
        s = "%s %s (%s)" % (self.user, self.full_name, self.email)
        return s

    class Admin:
        list_display = ('user', 'email', 'full_name')

    class Display:
        list_fields = (
                       ('User','user'),
                       ('Full_name','full_name'),
                       ('E-mail','email'),
                       )
        detail_fields = list_fields + ()


class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    status = models.TextField(choices = (
        ('REQUESTED','Requested'),
        ('GRANTED', 'Granted'),
        ('IN_USE', 'In use'),
        ('COMPLETED', 'Completed'),
        ('INVALID', 'Invalid'),
        ('FREE_REQUESTED', 'Free requested')))
    user = models.ForeignKey(User, db_column='user', on_delete = models.CASCADE)
    time_requested = models.DateTimeField()
    time_granted = models.DateTimeField(null=True, blank=True)
    time_completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'requests'

    class Admin:
        list_display = ('request_id', 'user', 'status', 'time_requested', 'time_granted', 'time_completed')
        list_filter = ['status', 'user', ]

    def __str__(self):
        s = "%s - %s" % (str(self.request_id), self.user_id)
        if self.status == 'COMPLETED' or self.status == 'INVALID':
            s = "(%s)" % s
        return s

    class Display:
        list_fields = (('User','user'),
                       ('Status','status'),
                       ('Time Requested','time_requested'),
                       ('Time Granted','time_granted'),
                       ('Time Completed','time_completed'),
                       ('Constraints', 'constraints', 'listbr'))

        detail_fields = list_fields + ()
        filter_fields = ('user','status') # resources filter added in views.py


class Chip(models.Model):
    chip_id = models.AutoField(primary_key=True)
    chip_name = models.CharField(max_length=100)
    class Meta:
        db_table = 'chips'
    def __str__(self):
        return self.chip_name


class Location(models.Model):
    location = models.CharField(primary_key=True, max_length=255)
    class Meta:
        db_table = 'location'
    def __str__(self):
        return self.location


class PlatformType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100)
    class Meta:
        db_table = 'platform_types'
    def __str__(self):
        return self.type_name


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(Request, null=True, blank=True, on_delete = models.SET_NULL)
    description = models.CharField(max_length=255)
    network_ip = models.CharField(max_length=255,unique=True)
    power_ip_port = models.CharField(max_length=255)
    console_ip_port = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)
    platform_type = models.ForeignKey(PlatformType, null=True, on_delete = models.SET_NULL)
    chip = models.ForeignKey(Chip, null=True, on_delete = models.SET_NULL)
    rev = models.CharField(max_length=100, null=True)
    sku = models.CharField(max_length=100, null=True)
    location = models.ForeignKey(Location, db_column='location', on_delete = models.CASCADE, default='Gdansk')
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    comment = models.TextField(max_length=100, null=True)
    workspace = models.CharField(max_length=100, null=True)
    last_request = models.CharField(max_length=100, null=True)
    time_owned = models.DurationField(null=True)

    def ip(self):
        return "%s" % (self.network_ip)
    ip.admin_order_field = 'network_ip'

    def power(self):
        return "%s" % (self.power_ip_port)
    power.admin_order_field = 'power_ip_port'

    def console(self):
        return "%s" % (self.console_ip_port)
    console.admin_order_field = 'console_ip_port'

    def chiprev(self):
        return "%s %s" % (self.chip, self.rev)
    chiprev.admin_order_field = 'chip,rev'

    class Meta:
        db_table = 'resources'
        ordering = ('description', 'comment')

    def __str__(self):
        return "%s" % (self.description)

    class Admin:
        list_display = ('description', 'network_ip', 'platform_type', 'chip', 'rev', 'position')
        list_filter = ['is_available', 'chip']
        search_fields = ['description']
        fields = (
            (None, {
                'fields' : ('description', ('is_available',
                    'is_reserved'), ('network_ip'))
            }),
            ('Extra', {
                'fields' : ('request')
            }),
            ('Connections', {
                'fields' : (('power_ip_port'), ('console_ip_port'))
            }),
            ('Type', {
                'fields' : ('platform_type', 'chip', 'rev')
            }),
            (None, {
                'fields' : ('comment', )
            }),
        )

    class Display:
        list_fields = (('Description','description'),
                       ('Network IP','ip'),
                       ('Console Server:Port','console_ip_port'),
                       ('Owner','owner'),
                       ('Platform','platform_type'),
                       ('Chip','chiprev'))
        detail_fields = list_fields + (('Comment', 'comment'))
        filter_fields = ('owned_by','platform','chip','location')


class TopologyClass(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)
    node_count = models.IntegerField

    class Meta:
        db_table = 'topology_class'

    def __str__(self):
        return self.class_name


class TopologyInstances(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(TopologyClass, null=True, blank=True, on_delete = models.SET_NULL)

    class Meta:
        db_table = 'topology_instances'


class ResourcesConnections(models.Model):
    topo_node_id = models.AutoField(primary_key=True)
    topo_instance = models.ForeignKey(TopologyInstances, on_delete = models.CASCADE)
    topo_node_index = models.IntegerField()
    topo_node_resource = models.ForeignKey(Resource, db_column='resources', on_delete = models.CASCADE)

    class Meta:
        db_table = 'resources_connections'

    def __str__(self):
        return "%d - %s" % (self.topo_node_index, str(self.topo_node_resource))
