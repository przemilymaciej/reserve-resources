from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.http.response import JsonResponse
from django.shortcuts import render, redirect


from .models import Resource, Request, User
from .filters import ResourceFilter
from django.utils import timezone

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


def release_resources(request):
    if request.method == 'POST':
        items = request.POST.get('items')
        to_find = items.split(',')[1:]

        for id in to_find:
            el = Resource.objects.get(pk=id)
            el.request_id = None
            el.status = 'FREE_REQUESTED'
            el.save()

        return JsonResponse({'status': 'Resource released'})

    return redirect('/')


def reserve_resources(request):
    if request.method == 'POST':
        items = request.POST.get('items')
        user_name = request.POST.get('user')
        to_find = items.split(',')[1:]

        try:
            owner = User.objects.get(user = user_name)
        except User.DoesNotExist:
            return JsonResponse({'message': 'This user doesnt exist in our database!'}, status=400)

        reserved_list = []
        for id in to_find:
            el = Resource.objects.get(pk=id)
            req = el.request_id

            if req:
                reserved_list.append(id)

        if len(reserved_list) > 0:
            if len(reserved_list) == 1:
                message = f'Platform {reserved_list[0]} is already reserved'
            else:
                message = f'Platforms {reserved_list} are already reserved'

            return JsonResponse({'message': message}, status=400)

        new_request = Request(status='GRANTED', user=owner, time_requested=timezone.now(), time_granted = timezone.now())
        new_request.save()

        for id in to_find:
            el = Resource.objects.get(pk=id)
            el.request_id = new_request
            el.save()

        return JsonResponse({'user': str(owner)})

    return redirect('/')