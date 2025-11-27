from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', views.getRoutes, name='api-routes'),
    path('projects/', views.getProjects, name='api-projects'),
    path('project/<str:pk>/', views.getProject, name='api-project-detail'),
    path('project/<str:pk>/vote/', views.projectVote, name='api-vote-project'),
    path('removetags/', views.removetags, name='api-tags'),
]