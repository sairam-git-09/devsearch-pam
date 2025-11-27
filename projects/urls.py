from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<uuid:pk>/', views.project, name='project'),
    path('create-project/', views.createProject, name='create-project'), 
    path('update-project/<uuid:pk>', views.updateProject, name='update-project'),
    path('delete-project/<uuid:pk>', views.deleteProject, name='delete-project'),
]