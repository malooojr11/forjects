from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from . import models
from . import forms


# Create your views here.
class ProjectListView(ListView):
    model = models.Project
    context_object_name = 'model'
    template_name = 'project/list.html'
    paginate_by = 4
    def get_queryset(self):
        query_set = super().get_queryset()
        where = {}
        q = self.request.GET.get('q', None)
        if q:
            where['title__icontains'] = q
            return query_set.filter(**where)
        return query_set

class ProjectCreateView(CreateView):
    model = models.Project
    context_object_name = 'project'
    form_class = forms.ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('Project_list')

class ProjectUpdateView(UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/update.html'


    def get_success_url(self):
        return reverse('Project_update',args=[self.object.id])

class TaskCreateView(CreateView):
    model = models.Task
    context_object_name = 'project'
    fields = ['project','description','title']
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('Project_update',args=[self.object.project.id])



class TaskUpdateView(UpdateView):
    model = models.Task
    context_object_name = 'project'
    fields = ['is_completed']
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('Project_update',args=[self.object.project.id])


class TaskDeleteView(DeleteView):
    model = models.Task

    def get_success_url(self):
        return reverse('Project_update',args=[self.object.project.id])


class ProjectDeleteView(DeleteView):
    model = models.Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('Project_list')