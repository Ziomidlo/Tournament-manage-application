from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewUserForm, TeamForm, UserForm, InvitationForm, AcceptInvitationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from invitations.models import Invitation
from django.db.models import Q
from itertools import chain

from .models import Tournament, User, Team


def navbar(request):
    logged_in_user = request.session.get('logged_in_user', None)
    if logged_in_user:
        user = User.objects.get(id=logged_in_user)
        context = {'user': user}
    else:
        user = None
    return render(request, 'tournament_app/navbar.html', context=context)

def index(request):
    return render(request, 'tournament_app/index.html')

def user_list(request):
    user_list = User.objects.order_by('id')
    return render(request, 'tournament_app/user_list.html', context={'user_list': user_list})

def user_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'tournament_app/user.html', context={'user': user})


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
            request.session['logged_in_user'] = user.id
            request.session.get('logged_in_user', None)
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
            user = authenticate(request, username=username, password = password)
            if user is not None:
                login(request, user)
                request.session['logged_in_user'] = user.id
                request.session.get('logged_in_user', None)
                messages.info(request, 'Jesteś zalogowany jako {username}.')
                return redirect('tournament_app:index')
            else: 
                messages.error(request, 'błędna nazwa użytkownika lub hasło!')
        else:
            messages.error(request,'błędna nazwa użytkownika lub hasło!')
    form = AuthenticationForm()
    return render(request=request, template_name='tournament_app/login.html', context={'login_form': form})
        

def logout_request(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
    logout(request)
    messages.info(request, 'Pomyślnie wylogowano.')
    return redirect('tournament_app:index')

@login_required(login_url='/login', redirect_field_name='next')
def create_team(request):
    if(request.user.is_team):
        return redirect('tournament_app:index' )
    else:
        if request.method == 'POST':
            form = TeamForm(request.POST, request.FILES)
            if form.is_valid():
                team = form.save(commit=False)
                team.leader = request.user
                User.objects.filter(pk=request.user.id).update(is_team=True)
                team.save()
                team.players.add(request.user)
                return redirect('tournament_app:team_details', pk=team.pk)
        else:
            form = TeamForm
        return render(request, 'tournament_app/create_team.html', context={'form': form})

@login_required(login_url='/login', redirect_field_name='next')
def update_team(request, pk): 
        team = get_object_or_404(Team, pk=pk)
        form = TeamForm(request.POST or None, request.FILES, instance=team)
        if request.user.id != team.leader.id:
            return render(request, 'tournament_app/index.html')
        else:
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('tournament_app:team_details', pk = team.pk)
                else:
                    return redirect('tournament_app:index.html')
            else: 
                form = TeamForm(instance=team)
            return render(request, 'tournament_app/update_team.html', context={'team': team, 'form': form})

@login_required(login_url='/login')
def delete_team(request,pk):
    team = get_object_or_404(Team, pk=pk)
    if request.user.id != team.leader.id:
        return render(request, 'tournament_app/index.html')
    else:
        if request.method == 'POST':
            team.delete()
            User.objects.filter(pk=request.user.id).update(is_team = False)
            return redirect('tournament_app:team_list')
        return render(request, 'tournament_app/delete_team.html', context={'team': team})

@login_required(login_url='/login')
def update_user(request, pk):
    user = get_object_or_404(User,pk=pk)
    form = UserForm(request.POST or None, request.FILES, instance=user)
    if request.user != user:
        return redirect('tournament_app:index')
    else: 
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('tournament_app:index')
            else:
                return redirect('tournament_app:index')
        else:
            form = UserForm(instance=user)
        return render(request, 'tournament_app/update_user.html', context={'user': user, 'form': form})

@login_required(login_url='/login')
def invite_user(request,pk):
    team = get_object_or_404(Team,pk=pk)
    form = InvitationForm(request.POST or None)

    if request.user.id != team.leader.id:
        return redirect('tournament_app:index')
    else:
        if request.method == 'POST':
            if form.is_valid():
                invitation = form.save(commit=False)
                messages.success(request, 'Zaproszenie zostało wysłane')
                invitation.team = team
                invitation.sender = request.user
                try:
                    recipient = User.objects.get(username=form.cleaned_data['recipient'])
                except User.DoesNotExist:
                    messages.error(request, 'Podany użytkownik nie istnieje')
                    return redirect('tournament_app:invite_user', pk=pk)
                if recipient in team.players.all():
                    messages.error(request, 'Użytkownik jest już w drużynie')
                    return redirect('tournament_app:invite_user', pk=pk)
                if team.players.count() >= 5:
                    messages.error(request, 'Drużyna już osiągnęła maksymalny limit zawodników')
                    return redirect('tournament_app:invite_user', pk=pk)
                invitation.recipient = recipient
                invitation.save()
                messages.success(request, 'Zaproszenie zostało wysłane')
                return redirect('tournament_app:index')
            else:
                form = InvitationForm()
        else:
            form = InvitationForm()
    return render(request, 'tournament_app/invite_user.html', context={'form': form, 'team': team})


@login_required(login_url='/login')
def get_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.user != invitation.recipient:
        return redirect('tournament_app:index')
    else:
        form = AcceptInvitationForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                if form.cleaned_data['accept']:
                    invitation.accept()
                    invitation.team.players.add(request.user)
                    User.objects.filter(pk=request.user.id).update(is_team=True)
                    invitation.delete()
                    messages.success(request, 'Zaproszenie zostało zaakceptowane')
                else:
                    invitation.delete()
                    messages.success(request, 'Zaproszenie zostało odrzucone')
                return redirect('tournament_app:index')
        else:
            form = AcceptInvitationForm()
        return render(request, 'tournament_app/get_invitation.html', context={'form': form, 'invitation': invitation})

def search(request):
    query = request.GET.get('search')
    print(query)
    if query:
        teams = Team.objects.filter(name__icontains=query)
        users = User.objects.filter(username__icontains=query)
        tournaments = Tournament.objects.filter(name__icontains=query)
    else:
        teams = User.objects.none()
        users = User.objects.none()
        tournaments = Tournament.objects.none()
    return render(request, 'tournament_app/search.html', {'teams': teams, 'users': users, 'tournaments': tournaments, 'query':query})
# Create your views here.
