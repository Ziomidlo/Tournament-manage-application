from django.db import models
from django.contrib.auth.models import AbstractUser
from invitations.utils import get_invitation_model

class User(AbstractUser):
    logo = models.ImageField()
    info = models.CharField(max_length=1000)
    is_team = models.BooleanField(default=False)

class Team(models.Model):
    logo = models.ImageField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    is_tournament = models.BooleanField(default=False)
    players = models.ForeignKey(User, on_delete=models.CASCADE)
    team_leader = models.BooleanField()
    date = models.DateField(auto_now=True)

class Tournament(models.Model):
    logo = models.ImageField()
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    number_of_teams = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    mvp = models.BooleanField()
    date = models.DateTimeField(auto_now=True)






