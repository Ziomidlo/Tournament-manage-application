from django.db import models
from django.contrib.auth.models import AbstractUser
from invitations.utils import get_invitation_model
from django.urls import reverse

class User(AbstractUser):
    logo = models.ImageField(null=True, blank=True, upload_to="user/")
    info = models.TextField(max_length=2000, blank=True, null=True)
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
    date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('tournament_app:team_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Tournament(models.Model):
    logo = models.ImageField(null=True, blank=True, upload_to="tournament/")
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    number_of_teams = models.IntegerField()
    team = models.ManyToManyField(Team, related_name='tournaments', null=True, blank=True)
    mvp = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('tournament_app:tournament_details', kwargs={'pk': self.pk})

class Invitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient', to_field = 'username', verbose_name='Odbiorca')
    message = models.TextField(verbose_name='Wiadomość')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
    # Sprawdź, czy zaproszenie nie zostało już zaakceptowane lub odrzucone
        if self.accepted:
            return False
    # Sprawdź, czy drużyna nie osiągnęła już maksymalnego limitu zawodników
        if self.team.players.count() >= 5:
            return False
        return True

    
    def accept(self):
        # Sprawdź, czy zaproszenie jest ważne (np. czy nie zostało już zaakceptowane lub odrzucone)
        if self.is_valid():
            # Dodaj odbiorcę zaproszenia do drużyny
            self.team.players.add(self.recipient)
            # Oznacz zaproszenie jako zaakceptowane
            self.accepted = True
            self.save()

    def reject(self):
        self.accepted = False
        self.save()






