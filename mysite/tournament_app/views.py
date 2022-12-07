from django.shortcuts import render
from django.http import HttpResponse

from .models import UserProfile, Tournament


def index(request):
    latest_tournament_list = Tournament.objects.order_by('id')
    context = {'latest_tournament_list' : latest_tournament_list}
    return render(request, 'index.html', context)

def tournament_details(request, id):
    details = Tournament.objects.get(pk = id)
    context = {'details' : details}
    return render(request, 'tournament.html', context)





# Create your views here.
