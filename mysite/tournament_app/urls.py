from django.urls import path

from  . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tournament/<int:id>/', views.tournament_details, name='tournament_details'),
]