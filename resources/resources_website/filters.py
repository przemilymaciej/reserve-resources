import django_filters

from .models import Resource

class ResourceFilter(django_filters.FilterSet):
    class Meta:
        model = Resource
        fields = ['request_id__user', 'platform_type', 'chip', 'location']

ResourceFilter.base_filters['request_id__user'].label = 'User'