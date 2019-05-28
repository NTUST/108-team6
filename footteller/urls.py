from django.contrib import admin
from django.urls import path

from main.views import index, players, refresh_data, player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('players', players, name="players"),
    path('refresh_data', refresh_data, name="refresh_data"),
    path('player', player, name="player"),
]
