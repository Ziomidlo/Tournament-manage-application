from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from .models import UserProfile, Tournament


def index(request):
    latest_tournament_list = Tournament.objects.order_by('id')
    context = {'latest_tournament_list' : latest_tournament_list}
    return render(request, 'tournament_app/index.html', context)

def tournament_details(request, pk):
    details = get_object_or_404(Tournament, pk = pk)
    context = {'details' : details}
    return render(request, 'tournament_app/tournament.html', context)





# Create your views here.
