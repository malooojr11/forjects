from django.http import Http404, HttpResponseRedirect  # Import Http404 exception
from django.shortcuts import render  # Import render function
from django.views.generic import ListView, CreateView, UpdateView, DeleteView  # Import generic views
from django.urls import reverse_lazy, reverse  # Import reverse functions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Import mixins
from . import models  # Import project models
from . import forms  # Import project forms


# Define views for the project app
class ProjectListView(LoginRequiredMixin, ListView):
    model = models.Project  # Set the model to Project
    context_object_name = 'model'  # Set the context object name
    template_name = 'project/list.html'  # Set the template name
    paginate_by = 4  # Set pagination limit

    def get_queryset(self):
        query_set = super().get_queryset()  # Get queryset from parent class

        # Filter projects based on the logged-in user
        query_set = query_set.filter(user=self.request.user)

        # Optionally, handle the case where the user is not authenticated
        if not self.request.user.is_authenticated:
            raise Http404("You must be logged in to view this page.")

        # Optionally, filter projects based on a search query (if provided)
        q = self.request.GET.get('q', None)
        if q:
            query_set = query_set.filter(title__icontains=q)

        return query_set


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project  # Set the model to Project
    context_object_name = 'project'  # Set the context object name
    form_class = forms.ProjectCreateForm  # Set the form class
    template_name = 'project/create.html'  # Set the template name
    success_url = reverse_lazy('Project_list')  # Set the success URL

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the current user to the project
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Project  # Set the model to Project
    form_class = forms.ProjectUpdateForm  # Set the form class
    template_name = 'project/update.html'  # Set the template name

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user  # Check if user is the project owner

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.id])  # Get success URL


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Task  # Set the model to Task
    context_object_name = 'project'  # Set the context object name
    fields = ['project', 'description', 'title']  # Set the fields to display
    http_method_names = ['post']  # Set allowed HTTP methods

    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return models.Project.objects.get(pk=project_id).user.id == self.request.user.id  # Check if user is the project owner

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id])  # Get success URL


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Task  # Set the model to Task
    context_object_name = 'project'  # Set the context object name
    fields = ['is_completed']  # Set the fields to display
    http_method_names = ['post']  # Set allowed HTTP methods

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user  # Check if user is the project owner

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id])  # Get success URL


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Task
    def test_func(self):
            task = self.get_object()
            return task.project.user == self.request.user

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id])


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Project  # Set the model to Project
    template_name = 'project/delete.html'  # Set the template name
    success_url = reverse_lazy('Project_list')  # Set the success URL

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user  # Check if user is the project owner
