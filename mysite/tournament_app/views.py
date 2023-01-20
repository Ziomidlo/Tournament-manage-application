from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewUserForm, TeamForm, UserForm, InvitationForm, AcceptInvitationForm, WinnerTeam, MVPForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from random import shuffle

from .models import Tournament, User, Team, Invitation, Match


def index(request):
    return render(request, 'tournament_app/index.html')

def user_list(request):
    user_list = User.objects.order_by('id')
    return render(request, 'tournament_app/user_list.html', context={'user_list': user_list})

def user_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'tournament_app/user.html', context={'user': user})

def tournament_list(request):
    tournaments = Tournament.objects.order_by('id')
    return render(request, 'tournament_app/tournaments.html', context = {'tournaments' : tournaments})

def tournament_details(request, pk):
    tournament_details = get_object_or_404(Tournament, pk = pk)
    return render(request, 'tournament_app/tournament.html', context = {'tournament' : tournament_details})

def team_list(request):
    team_list = Team.objects.order_by('id')
    return render(request, 'tournament_app/teams.html', context= {'team_list': team_list})

def team_details(request, pk):
    team_details = get_object_or_404(Team, pk = pk)
    return render(request, 'tournament_app/team.html', context = {'team': team_details})

def match_details(request, tournament_pk, match_pk):
    tournament = get_object_or_404(Tournament, pk=tournament_pk)
    match = get_object_or_404(Match, pk=match_pk)
    return render(request, 'tournament_app/match.html', context={'tournament': tournament, 'match': match})

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
                messages.success(request, 'Pomyślnie zalogowano!')
                return redirect('tournament_app:index')
            else: 
                messages.error(request, 'Błędna nazwa użytkownika lub hasło!')
        else:
            messages.error(request,'Błędna nazwa użytkownika lub hasło!')
    form = AuthenticationForm()
    return render(request=request, template_name='tournament_app/login.html', context={'login_form': form})
        

def logout_request(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano.')
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
                messages.success(request, 'Pomyślnie utworzono drużynę!')
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
                    messages.success(request, 'Pomyślnie zaktualizowano dane drużyny!')
                    return redirect('tournament_app:team_details', pk = team.pk)
                else:
                    messages.error(request, 'Nie udało się zaktualizować danych drużyny!')
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
            for player in team.players.all():
                player.is_team = False
                player.save()
            team.delete()
            messages.success(request, 'Pomyślnie usunięto drużynę!')
            return redirect('tournament_app:index')
        return render(request, 'tournament_app/delete_team.html', context={'team': team})

@login_required(login_url='/login')
def remove_player(request, team_pk, player_pk):
    team = get_object_or_404(Team, pk=team_pk)
    player = get_object_or_404(User, pk=player_pk)
    if request.user.id != team.leader.id or player not in team.players.all():
        messages.error(request, 'Nie masz do tego dostępu!')
        return render(request, 'tournament_app/index.html')
    if request.method == 'POST':
        team.players.remove(player)
        User.objects.filter(pk=player_pk).update(is_team=False)
        messages.success(request, f'{player.username} został usunięty z drużyny {team.name}')
        return redirect('tournament_app:team_details', pk=team.pk)
    else:
        return render(request, 'tournament_app/remove_player.html', context={'team': team, 'player': player})

@login_required(login_url='/login')
def leave_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    user = request.user
    if request.user.id == team.leader.id:
        messages.error(request, 'Nie możesz wyjść, jesteś liderem tej drużyny!')
        return redirect('tournament_app:index')
    if request.method == 'POST':
        if user.is_team and user in team.players.all():
            team.players.remove(user)
            User.objects.filter(pk=user.id).update(is_team=False)
            messages.success(request, 'Opuściłeś drużynę')
            return redirect('tournament_app:index')
        else:
            messages.error(request, 'Nie jesteś w tej drużynie!')
            return redirect('tournament_app:index')
    else:
        return render(request, 'tournament_app/leave_team.html', context={'team': team})



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
                messages.success(request, 'Pomyślnie zaktualizowałeś Swoje dane!')
                return redirect('tournament_app:index')
            else:
                messages.error(request, 'Coś poszło nie tak!')
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
                invitation.team = team
                invitation.sender = request.user
                try:
                    recipient = User.objects.get(username=form.cleaned_data['recipient'])
                except User.DoesNotExist:                    
                    messages.error(request, 'Podany użytkownik nie istnieje!')
                    return redirect('tournament_app:invite_user', pk=pk)
                if recipient in team.players.all():
                    messages.error(request, 'Użytkownik jest już w drużynie!')
                    return redirect('tournament_app:invite_user', pk=pk)
                if team.players.count() >= 5:
                    messages.error(request, 'Drużyna już osiągnęła maksymalny limit zawodników!')
                    return redirect('tournament_app:invite_user', pk=pk)
                if Invitation.objects.filter(recipient=recipient, team=team).exists():
                    messages.error(request, 'Użytkownik ma już zaproszenie od tej drużyny!')
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
                accept = form.cleaned_data['accept']
                if accept == 'Tak':
                    invitation.accept()
                    invitation.team.players.add(request.user)
                    User.objects.filter(pk=request.user.id).update(is_team=True)
                    invitation.delete()
                    messages.success(request, 'Zaproszenie zostało zaakceptowane')
                else:
                    print(accept)
                    invitation.delete()
                    messages.success(request, 'Zaproszenie zostało odrzucone')
                return redirect('tournament_app:index')
        else:
            form = AcceptInvitationForm()
        return render(request, 'tournament_app/get_invitation.html', context={'form': form, 'invitation': invitation})

def search(request):
    query = request.GET.get('search')
    if query:
        teams = Team.objects.filter(name__icontains=query)
        users = User.objects.filter(username__icontains=query)
        tournaments = Tournament.objects.filter(name__icontains=query)
    else:
        teams = User.objects.none()
        users = User.objects.none()
        tournaments = Tournament.objects.none()
    return render(request, 'tournament_app/search.html', {'teams': teams, 'users': users, 'tournaments': tournaments, 'query':query})

@login_required(login_url='/login')
def join_tournament(request, tournament_pk, team_pk):
    tournament = get_object_or_404(Tournament, pk=tournament_pk)
    team = get_object_or_404(Team, pk=team_pk)
    if request.user.id != team.leader.id:
        messages.error(request, 'Tylko lider drużyny może dołączyć do turnieju!')
        return redirect('tournament_app:tournament_details', pk=tournament_pk)
    else:
        if request.method == 'POST':  
            if team in tournament.team.all() and team.is_tournament:
                messages.error(request, 'Twoja drużyna już bierze udział w turnieju!')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
            elif team.players.count() != 5:
                messages.error(request, 'By uczestniczyć w tym turnieju musisz posiadać 5 graczy!')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
            elif tournament.is_started:
                messages.error(request, 'Nie można dołączyć do trwającego turnieju!')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
            elif tournament.team.count() >= tournament.number_of_teams:
                messages.error(request, 'Turniej jest już pełny!')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
            else:
                tournament.team.add(team)
                Team.objects.filter(pk=team_pk).update(is_tournament=True)
                tournament.save()
                messages.success(request, 'Twoja drużyna dołączyła do turnieju!')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
        else:
            return render(request,'tournament_app/join_tournament.html', context= { 'tournament': tournament, 'team': team})

@login_required(login_url='/login')
def leave_tournament(request, tournament_pk, team_pk):
    tournament = get_object_or_404(Tournament, pk=tournament_pk)
    team = get_object_or_404(Team, pk=team_pk)
    if request.user.id != team.leader.id:
        messages.error(request, 'Tylko lider drużyny może opuścić turniej!')
        return redirect('tournament_app:tournament_details', pk=tournament_pk)
    else:
        if request.method == 'POST':  
            if tournament.is_started == True:
                messages.error(request, 'Nie można opuścić trwającego turnieju!')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
            else:  
                tournament.team.remove(team)
                Team.objects.filter(pk=team.pk).update(is_tournament=False)
                tournament.save()
                messages.success(request, 'Twoja drużyna pomyślnie opuściła turniej!')
                return redirect('tournament_app:team_details', pk=team_pk)
        else:
            return render(request,'tournament_app/leave_tournament.html', context= { 'tournament': tournament, 'team': team})

@login_required(login_url='/login')
def start_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    user = request.user
    if user.is_superuser == False:
        messages.error(request, 'Nie masz do tego dostępu!')
        return redirect('tournament_app:tournament_details', pk=pk)
    else:
        if request.method == 'POST':
            if tournament.is_started:
                messages.error(request, 'Turniej już wystartował!')
                return redirect('tournament_app:tournament_details', pk=pk)
            elif tournament.team.count() != tournament.number_of_teams:
                messages.error(request, 'Niewystarczająca ilość drużyn!')
                return redirect('tournament_app:tournament_details', pk=pk)
            else:
                Tournament.objects.filter(pk=pk).update(is_started=True)
                messages.success(request, 'Turniej pomyślnie wystartował!')
                return redirect('tournament_app:tournament_details', pk=pk)
        else:
            return render(request,'tournament_app/start_tournament.html', context= { 'tournament': tournament})



@login_required(login_url='/login')
def finish_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    user = request.user
    if user.is_superuser == False:
        messages.error(request, 'Nie masz do tego dostępu!')
        return redirect('tournament_app:tournament_details', pk=pk)
    else:
        if request.method == 'POST':
            if tournament.is_finished == False:
                messages.error(request, 'Turniej się jeszcze nie zakończył!')
                return redirect('tournament_app:tournament_details', pk=pk)
            else:
                remaining_team = tournament.team.first()
                remaining_team.is_tournament = False
                remaining_team.won_tournaments += 1
                remaining_team.save()
                if remaining_team.players.count() > 0:
                    form = MVPForm(remaining_team, data=request.POST)
                    if form.is_valid():
                        MVP = form.cleaned_data['MVP']
                        MVP.MVP += 1
                        MVP.save()
                        tournament.MVP = MVP
                        tournament.save()
                        messages.success(request, f'{MVP} został MVP turnieju!')
                    else:
                        messages.error(request, 'Formularz MVP jest nieprawidłowy')
                        return redirect('tournament_app:tournament_details', pk=pk)
                else:
                    messages.error(request, 'Brak graczy w drużynie')
                tournament.save()
                tournament.delete()
                messages.success(request, 'Pomyślnie zakończono turniej!')
                return redirect('tournament_app:index')
        else:
            remaining_team = tournament.team.first()
            if remaining_team.players.count() > 0:
                form = MVPForm(remaining_team)
                return render(request, 'tournament_app/finish_tournament.html', {'form': form, 'tournament': tournament})
            else:
                messages.error(request, 'Brak graczy w drużynie')
                return redirect('tournament_app:tournament_details', pk=pk)


@login_required(login_url='/login')
def randomize_teams(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    teams = list(tournament.team.all())
    user = request.user
    if user.is_superuser == False:
        messages.error(request, 'Nie masz do tego dostępu!')
        return redirect('tournament_app:tournament_details', pk=pk)
    if tournament.is_started == False:
        messages.error(request, 'Turniej się jeszcze nie rozpoczął!')
        return redirect('tournament_app:tournament_details', pk=pk)
    if tournament.is_drawed:
        messages.error(request, 'Drużyny już zostały wylosowane!')
        return redirect('tournament_app:tournament_details', pk=pk)
    shuffle(teams)
    for i in range(0, len(teams), 2):
        home_team = teams[i]
        away_team = teams[i+1]
        match = Match(tournament=tournament, home_team=home_team, away_team=away_team)
        match.save()
    tournament.save()
    Tournament.objects.filter(pk=pk).update(is_drawed=True)
    messages.success(request, 'Drużyny zostały losowo przydzielone')
    return redirect('tournament_app:tournament_details', pk=pk)

@login_required(login_url='/login')
def finish_round(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    user = request.user
    if user.is_superuser == False:
        messages.error(request, 'Nie masz do tego dostępu!')
        return redirect('tournament_app:tournament_details', pk=pk)
    elif tournament.is_drawed == False:
        messages.error(request, 'Nie rozlosowano drużyn!')
        return redirect('tournament_app:tournament_details', pk=pk)
    else:
        if not all(match.is_finished for match in tournament.matches.all()):
            messages.error(request, 'Nie wszystkie mecze zostały zakończone, nie można skończyć rundy!')
            return redirect('tournament_app:tournament_details', pk=pk)
        else:
            tournament.matches.all().delete()
            tournament.round_number += 1
            tournament.save()
            if tournament.team.count() == 1:
                tournament.is_finished = True
                tournament.save()
            Tournament.objects.filter(pk=pk).update(is_drawed=False)
            messages.success(request, 'Pomyślnie zakończono rundę.')
            return redirect('tournament_app:tournament_details', pk=pk)


@login_required(login_url='/login')
def save_match(request, tournament_pk, match_pk):
    tournament = get_object_or_404(Tournament, pk=tournament_pk)
    match = get_object_or_404(Match, pk=match_pk)
    user = request.user
    if user.is_superuser == False:
        messages.error(request, 'Nie masz do tego dostępu!')
        return redirect('tournament_app:tournament_details', pk=tournament_pk)
    elif match.is_finished == True:
        messages.error(request, 'Mecz się już zakończył!')
        return redirect('tournament_app:tournament_details', pk=tournament_pk)
    else:
        if request.method == 'POST':
            form = WinnerTeam(request.POST)
            if form.is_valid():
                match.winner = form.cleaned_data['winner']
                print(match.winner)
                if match.winner == match.home_team:
                    tournament.team.remove(match.away_team)
                    tournament.save()
                    match.away_team.is_tournament = False
                elif match.winner == match.away_team:
                    home_team = Match.objects.filter(pk=match_pk).first().home_team
                    tournament.team.remove(match.home_team)
                    tournament.save()
                    home_team.is_tournament = False 
                match.is_finished = True
                match.save()
                tournament.save()
                messages.success(request, f'Pomyślnie zapisano wynik, wygrana drużyny! {match.winner}')
                return redirect('tournament_app:tournament_details', pk=tournament_pk)
            else:
                messages.error(request, 'Niepoprawnie zapisano wynik!')
                return redirect('tournament_app:match_details', tournament_pk=tournament_pk, match_pk=match_pk)
        else:
            form = WinnerTeam(request.POST)
        return render(request,'tournament_app/match.html', context= { 'match':match, 'tournament':tournament, 'form':form })
    

# Create your views here.
