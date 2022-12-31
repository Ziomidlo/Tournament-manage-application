from django.contrib import admin

from .models import Tournament, Team, User, Invitation

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Invitation)

# Register your models here.
