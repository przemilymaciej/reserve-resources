from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.http.response import JsonResponse
from django.shortcuts import render, redirect


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


# class AjaxHandlerView(View):
#     def post(self, request):
#         id = request.GET.get('id')
#         print(id)
#         return render(request, 'resources_website/index.html')

# def release_resources(request):
#     # print(request.GET['id'])
#     print("sialala")

# def release_resources(request):
#     if request.method == 'GET':
#            post_id = request.GET['post_id']
#            return HttpResponse("Success!") # Sending an success response
#     else:
#            return HttpResponse("Request method is not a GET")

def release_resources(request):
    if request.method == 'POST':
        items = request.POST.get('items')
        to_find = items.split(',')[1:]

        for id in to_find:
            el = Resource.objects.get(pk=id)
            el.request_id = None
            el.save()

        return JsonResponse({'status': 'Resource released'})

    return redirect('/')