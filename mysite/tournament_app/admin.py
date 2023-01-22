from django.contrib import admin

from .models import Tournament, Team, User, Invitation

class TournamentAdmin(admin.ModelAdmin):
    exclude = ['is_started', 'round_number', 'is_finished', 'is_drawed']


class UserAdmin(admin.ModelAdmin):
    exclude = ['MVP']

class InvitationAdmin(admin.ModelAdmin):
    exclude = ['accepted']

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team)
admin.site.register(User, UserAdmin)
admin.site.register(Invitation, InvitationAdmin)
# Register your models here.
