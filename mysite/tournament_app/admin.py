from django.contrib import admin

from .models import Tournament, Team, User

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(User)

# Register your models here.
