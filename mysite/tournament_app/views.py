from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


from .models import Tournament, User


def index(request):
    return render(request, 'tournament_app/index.html')

def tournament_list(request):
    latest_tournament_list = Tournament.objects.order_by('id')
    context = {'latest_tournament_list' : latest_tournament_list}
    return render(request, 'tournament_app/tournaments.html', context)

def tournament_details(request, pk):
    tournament_details = get_object_or_404(Tournament, pk = pk)
    context = {'tournament' : tournament_details}
    return render(request, 'tournament_app/tournament.html', context)

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
            messages.error(request,'błędna nazwa użytkownika lub hasło!')
    form = AuthenticationForm()
    return render(request=request, template_name='tournament_app/login.html', context={'login_form': form})

def logout_request(request):
    logout(request)
    messages.info(request, 'Pomyślnie wylogowano.')
    return redirect('tournament_app:index')







# Create your views here.
