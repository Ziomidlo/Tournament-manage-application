from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from  . import views

app_name = 'tournament_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.user_list, name='user_list'),
    path('user/<int:user_id>/', views.user_details, name='user_details'),
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
    path('update_user/<int:pk>/', views.update_user, name='update_user'),
    path('invite_user/<int:pk>/', views.invite_user, name='invite_user'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
