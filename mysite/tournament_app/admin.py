from django.contrib import admin

from .models import Tournament, Team, User, Invitation

class TournamentAdmin(admin.ModelAdmin):
    exclude = ['is_drawed', 'is_finished', 'is_started', 'round_number']

class TeamAdmin(admin.ModelAdmin):
    exclude = ['is_tournament']

class UserAdmin(admin.ModelAdmin):
    exclude = ['is_team', 'MVP']

class InvitationAdmin(admin.ModelAdmin):
    exclude = ['accepted']

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Invitation, InvitationAdmin)
# Register your models here.
