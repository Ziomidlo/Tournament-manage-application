from django.db import models
from django.contrib.auth.models import AbstractUser
from invitations.utils import get_invitation_model
from django.urls import reverse
from django.core.exceptions import ValidationError

class User(AbstractUser):
    logo = models.ImageField(null=True, blank=True, upload_to="user/")
    info = models.TextField(max_length=2000, blank=True, null=True)
    MVP = models.IntegerField(default=0)
    is_team = models.BooleanField(default=False, blank = True)

    def get_absolute_url(self):
        return reverse('tournament_app:user_details', kwargs={'pk': self.pk})

class Team(models.Model):
    logo = models.ImageField(null=True, blank=True, upload_to="team/")
    name = models.CharField(max_length=50, verbose_name='Nazwa drużyny')
    description = models.TextField(max_length=2000, verbose_name='Opis drużyny')
    is_tournament = models.BooleanField(default=False, blank=True)
    players = models.ManyToManyField(User, related_name='teams', null=True, blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams', verbose_name='Lider')
    won_tournaments = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('tournament_app:team_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


def power_of_two(value):
    if (value & (value - 1) != 0):
        raise ValidationError("Wartość musi być potęgą dwójki!")


class Tournament(models.Model):
    logo = models.ImageField(null=True, blank=True, upload_to="tournament/")
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    number_of_teams = models.IntegerField(validators=[power_of_two])
    team = models.ManyToManyField(Team, related_name='tournaments', null=True, blank=True)
    is_started = models.BooleanField(default=False, blank=True)
    is_finished = models.BooleanField(default=False, blank=True)
    is_drawed = models.BooleanField(default=False, blank=True)
    round_number = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now=True)
    MVP = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tournament_MVP', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('tournament_app:tournament_details', kwargs={'pk': self.pk})

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches', null=True)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches', null=True)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='winning_matches', null=True, blank=True)
    is_finished = models.BooleanField(default=False)


class Invitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'recipient', to_field = 'username', verbose_name='Odbiorca')
    title = models.CharField(max_length=150, verbose_name='Tytuł')
    message = models.TextField(verbose_name='Wiadomość')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        if self.accepted:
            return False
        if self.team.players.count() >= 5:
            return False
        return True

    
    def accept(self):
        if self.is_valid():
            self.team.players.add(self.recipient)
            self.accepted = True
            self.save()

    def reject(self):
        self.accepted = False
        self.save()






