from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Resource
from .filters import ResourceFilter

class FilteredListView(generic.ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filterset'] = self.filterset
        return context

class IndexView(generic.ListView):
    model = Resource
    template_name = 'resources_website/index.html'
    filterset_class = ResourceFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        myFilter = ResourceFilter(self.request.GET.get(''), queryset=self.get_queryset().order_by('resource_id'))

        resources = myFilter.qs

        context['resources'] = resources
        context['myFilter'] = myFilter
        return context