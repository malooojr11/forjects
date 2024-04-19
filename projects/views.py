from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models
from . import forms


# Create your views here.
class ProjectListView(LoginRequiredMixin, ListView):
    model = models.Project
    context_object_name = 'model'
    template_name = 'project/list.html'
    paginate_by = 4

    def get_queryset(self):
        query_set = super().get_queryset()

        # Filter projects based on the logged-in user
        query_set = query_set.filter(user=self.request.user)

        # Optionally, you can handle the case where the user is not authenticated
        if not self.request.user.is_authenticated:
            raise Http404("You must be logged in to view this page.")

        # Optionally, you can also filter projects based on a search query (if provided)
        q = self.request.GET.get('q', None)
        if q:
            query_set = query_set.filter(title__icontains=q)

        return query_set


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    context_object_name = 'project'
    form_class = forms.ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('Project_list')


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/update.html'

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.id])


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Task
    context_object_name = 'project'
    fields = ['project', 'description', 'title']
    http_method_names = ['post']

    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return models.Project.objects.get(pk=project_id).user.id == self.request.user.id

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id])


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Task
    context_object_name = 'project'
    fields = ['is_completed']
    http_method_names = ['post']

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id])


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Task

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id])


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('Project_list')

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user
