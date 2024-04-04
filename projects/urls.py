from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProjectListView.as_view(), name='Project_list'),
    path('project/create',views.ProjectCreateView.as_view(),name='Project_create'),
    path('project/edite/<int:pk>', views.ProjectUpdateView.as_view(), name='Project_update'),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='Project_delete'),
    path('task/create', views.TaskCreateView.as_view(), name='Task_create'),
    path('task/edite/<int:pk>', views.TaskUpdateView.as_view(), name='Task_update'),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name='Task_delete'),

]
