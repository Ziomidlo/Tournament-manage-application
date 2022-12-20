from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from  . import views

app_name = 'tournament_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('tournaments', views.tournament_list, name ='tournament_list'),
    path('tournament/<int:pk>/', views.tournament_details, name='tournament_details'),
    path('teams', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_details, name='team_details'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login' ),
    path('logout', views.logout_request, name='logout'),
    path('create_team', views.create_team, name='create_team'),
    path('update_team/<int:pk>/', views.update_team, name='update_team'),
    path('delete_team/<int:pk>/', views.delete_team, name='delete_team'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
