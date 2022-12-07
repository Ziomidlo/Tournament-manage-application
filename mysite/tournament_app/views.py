from django.http import HttpResponse
from django.template import loader

from .models import UserProfile, Tournament


def index(request):
    latest_tournement_list = Tournament.objects.order_by('id')
    template = loader.get_template('tournament_app/index.html')
    context = {
        'latest_tournament_list': latest_tournement_list,
    }
    return HttpResponse(template.render(context, request))


# Create your views here.
