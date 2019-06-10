from django.contrib import admin
from django.urls import path

from analysis.views import predict, predict_result
from main.views import index, players, refresh_data, get_player, edit_team, get_team, create_player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('predict/', predict, name="predict"),
    path('analysis_form/', predict_result),
    path('players/create', create_player, name="create-player"),
    path('players', players, name="players"),
    path('players/<str:player_name>', get_player, name="player"),
    path('refresh_data', refresh_data, name="refresh_data"),
    path('team/', get_team, name="team"),
    path('team/edit', edit_team, name="edit-team"),

]
