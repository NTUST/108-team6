from django.contrib import admin

# Register your models here.
from main.models import Player, TeamPlayer


class TeamPlayerAdmin(admin.ModelAdmin):
    raw_id_fields = ('player', 'user')


admin.site.register(Player)
admin.site.register(TeamPlayer, TeamPlayerAdmin)
