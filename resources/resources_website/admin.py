from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Request)
admin.site.register(Chip)
admin.site.register(PlatformType)
admin.site.register(Resource)
admin.site.register(TopologyClass)
admin.site.register(TopologyInstances)
admin.site.register(ResourcesConnections)
