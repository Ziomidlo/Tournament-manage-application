from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Team, Invitation, Match, Tournament

User = get_user_model()

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = ("logo", "name", "description")

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ("logo", "info")

class InvitationForm(ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.filter(is_team=False), label='Użytkownik')
    
    class Meta:
        model = Invitation
        fields =  ("recipient", "title", "message")


class AcceptInvitationForm(forms.Form):
    accept = forms.ChoiceField(label='Czy zaakceptować zaproszenie?', choices=[('Tak', 'Tak'), ('Nie', 'Nie')], widget=forms.RadioSelect)

class WinnerTeam(ModelForm):
    
    class Meta:
        model = Match
        fields = ['winner']
    winner = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.RadioSelect, empty_label=None)

class MVPForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['MVP']

    def __init__(self, remaining_team, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MVP'].queryset = remaining_team.players.all()


    
    
    
