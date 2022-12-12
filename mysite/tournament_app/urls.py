from django.urls import path

from  . import views

app_name = 'tournament_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('tournaments', views.tournament_list, name ='tournament_list'),
    path('tournament/<int:pk>/', views.tournament_details, name='tournament_details'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login' ),
    path('logout', views.logout_request, name='logout'),
]