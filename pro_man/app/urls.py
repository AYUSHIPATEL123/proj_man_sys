from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('home/',home,name='home'),
    path('register/',register,name='register'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',log_out,name='logout'),
    path('project_list/',ProjectListView.as_view(),name='projects'),
    path('task_list/',TaskListView.as_view(),name='tasks'),
    path('comment_list/',CommentListView.as_view(),name='comments'),
    path('create_project/', ProjectCreateView.as_view(),name='project_create'),
    path('proj_detail/<int:pk>/',ProjectDetailView.as_view(),name='project_detail'),
    path('task_detail/<int:pk>/',TaskDetailView.as_view(),name='task_detail'),
    path('project_update/<int:pk>/',ProjectUpdateView.as_view(),name='project_update'),
    path('project_delete/<int:pk>/',ProjectDeleteView.as_view(),name='project_delete'),
    path('task_update/<int:pk>/',TaskUpdateView.as_view(),name='task_update'),
    path('task_delete/<int:pk>/',TaskDeleteView.as_view(),name='task_delete'),
    path('task_create/',TaskCreateView.as_view(),name='task_create'),
]
