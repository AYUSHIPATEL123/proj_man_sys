"""
URL configuration for pro_man project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('create_project/', ProjectCreateView.as_view(),name='create_project'),
    path('proj_detail/<int:pk>/',ProjectDetailView.as_view(),name='project_detail'),
    path('task_detail/<int:pk>/',TaskDetailView.as_view(),name='task_detail'),
    path('project_update/<int:pk>/',ProjectUpdateView.as_view(),name='project_update'),
    path('project_delete/<int:pk>/',ProjectDeleteView.as_view(),name='project_delete'),
    path('task_update/<int:pk>/',TaskUpdateView.as_view(),name='task_update'),
    path('task_delete/<int:pk>/',TaskDeleteView.as_view(),name='task_delete'),
]
