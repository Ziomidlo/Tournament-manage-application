from django.shortcuts import render
from django.http import HttpResponse

from .models import UserProfile, Torunament


def index(request):
    latest_tournement_list = Torunament.objects.order_by('id')
    output = '\n'.join([t.name for t in latest_tournement_list ])
    return HttpResponse(output)


# Create your views here.
