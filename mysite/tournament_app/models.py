from django.db import models
from django.contrib.auth.models import AbstractUser
from invitations.utils import get_invitation_model

class User(AbstractUser):
    logo = models.ImageField(null=True, blank=True, upload_to="user/")
    info = models.TextField(max_length=2000)
    is_team = models.BooleanField(default=False, blank = True)

class Team(models.Model):
    logo = models.ImageField(null=True, blank=True, upload_to="team/")
    name = models.CharField(max_length=50, verbose_name='Nazwa drużyny')
    description = models.TextField(max_length=2000, verbose_name='Opis drużyny')
    is_tournament = models.BooleanField(default=False, blank=True)
    players = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    leader = models.IntegerField(blank=False, default=1, verbose_name='Lider')
    date = models.DateField(auto_now=True)

class Tournament(models.Model):
    logo = models.ImageField(null=True, blank=True, upload_to="tournament/")
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    number_of_teams = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    mvp = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now=True)






