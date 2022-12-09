from django.urls import path

from  . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tournament/<int:pk>/', views.tournament_details, name='tournament_details'),
]