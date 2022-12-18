from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewUserForm, TeamForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


from .models import Tournament, User, Team


def index(request):
    return render(request, 'tournament_app/index.html')

@login_required(login_url='/login', redirect_field_name='torunament_list')
def tournament_list(request):
    latest_tournament_list = Tournament.objects.order_by('id')
    return render(request, 'tournament_app/tournaments.html', context = {'latest_tournament_list' : latest_tournament_list})

def tournament_details(request, pk):
    tournament_details = get_object_or_404(Tournament, pk = pk)
    return render(request, 'tournament_app/tournament.html', context = {'tournament' : tournament_details})

def team_list(request):
    team_list = Team.objects.order_by('id')
    return render(request, 'tournament_app/teams.html', context= {'team_list': team_list})

def team_details(request, pk):
    team_details = get_object_or_404(Team, pk = pk)
    return render(request, 'tournament_app/team.html', context = {'team': team_details})

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Pomyślnie zarejestrowano!')
            return redirect('tournament_app:index')
        messages.error(request, 'Rejestracja nieudana!')
    form = NewUserForm()
    return render(request=request, template_name='tournament_app/register.html', context={'register_form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, 'Jesteś zalogowany jako {username}.')
                return redirect('tournament_app:index')
            else: 
                messages.error(request, 'błędna nazwa użytkownika lub hasło!')
        else:
            messages.error(request,'błędna nazwa użytkownika lub hasło!')
    form = AuthenticationForm()
    return render(request=request, template_name='tournament_app/login.html', context={'login_form': form})
        

def logout_request(request):
    logout(request)
    messages.info(request, 'Pomyślnie wylogowano.')
    return redirect('tournament_app:index')

@login_required
def create_team(request):
    submitted = False
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = TeamForm
        if 'submitted' in request.GET:
            submitted = True


    return render(request, 'tournament_app/create_team.html', context={'form': form, 'submitted': submitted} )


# Create your views here.
