from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.http.response import JsonResponse
from django.shortcuts import render, redirect


from .models import Resource, Request, User
from .filters import ResourceFilter, RequestFilter
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


class RequestView(generic.ListView):
    model = Request
    template_name = 'resources_website/requests.html'
    filterset_class = RequestFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        myFilter = RequestFilter(self.request.GET.get(''), queryset=self.get_queryset().order_by('request_id'))

        requests = myFilter.qs

        context['requests'] = requests
        context['myFilter'] = myFilter
        return context


def release_resources(request):
    if request.method == 'POST':
        items = request.POST.get('items')
        to_find = items.split(',')[1:]
        times = []

        for id in to_find:
            el = Resource.objects.get(pk=id)
            request = Request.objects.get(pk=el.request_id.pk)
            request.time_completed = timezone.now()
            request.status = 'COMPLETED'
            request.save()
            diff = request.time_completed - request.time_granted
            el.time_owned = diff
            times.append(str(diff))
            el.request_id = None
            el.status = 'FREE_REQUESTED'
            el.is_available = 1
            el.is_reserved = 0
            el.save()

        return JsonResponse({'status': 'Resource released', 'times' : times})

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
            el.is_available = 0
            el.is_reserved = 1
            el.last_request = f'{new_request.request_id} - {owner.user}'
            el.save()

        return JsonResponse({'user': str(owner), 'request_id' : new_request.pk, 'user_name' : owner.user})

    return redirect('/')