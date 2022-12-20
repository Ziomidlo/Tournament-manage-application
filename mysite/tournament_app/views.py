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
    if request.user.is_authenticated:
        return redirect('tournament_app:index')

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
    if request.user.is_authenticated:
        return redirect('tournament_app:index')

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

@login_required(login_url='/login', redirect_field_name='next')
def create_team(request):
    submitted = False
    if(request.user.is_team):
        return redirect('tournament_app:index')
    else:
        if request.method == 'POST':
            form = TeamForm(request.POST, request.FILES)
            if form.is_valid():
                team = form.save(commit=False)
                team.leader = request.user.id
                User.objects.filter(pk=request.user.id).update(is_team=True)
                team.save()
                return HttpResponseRedirect('/create_team?submitted=True')
        else:
            form = TeamForm
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'tournament_app/create_team.html', context={'form': form, 'submitted': submitted} )

@login_required(login_url='/login', redirect_field_name='next')
def update_team(request, pk): 
        team = get_object_or_404(Team, pk = pk)
        form = TeamForm(request.POST or None, request.FILES, instance=team)
        if request.user.id != team.leader:
            return render(request, 'tournament_app/index.html')
        else:
            if request.method == 'POST':
                if request.user.id == team.leader:
                    if form.is_valid():
                        form.save()
                        return redirect('team_details', pk = team.pk)
                else:
                    return redirect('tournament_app:index.html')
            else:
                form = TeamForm
            return render(request, 'tournament_app/update_team.html', context={'team': team, 'form':form})

@login_required(login_url='/login')
def delete_team(request,pk):
    team = get_object_or_404(Team, pk=pk)
    if team.leader != request.user.id:
        return render(request, 'tournament_app/index.html')
    else:
        if request.method == 'POST':
            team.delete()
            User.objects.filter(pk=request.user.id).update(is_team = False)
            return redirect('tournament_app:index')
        return render(request, 'tournament_app/delete_team.html', context={'team': team})


# Create your views here.
