from django.contrib import admin
from django.urls import path

from analysis.views import predict, predict_result
from main.views import index, players, refresh_data, player, edit_team, team, create_player, login, login_form, \
    register, register_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('player', players, name="players"),
    path('player/<str:player_number>', player, name="player"),
    path('player/create', create_player, name="create-player"),
    path('predict/', predict, name="predict"),
    path('analysis_form/', predict_result),
    path('team/', team, name="team"),
    path('team/edit', edit_team, name="edit-team"),
    path('refresh_data', refresh_data, name="refresh_data"),
    path('login/', login),
    path('login_form/', login_form),
    path('register/', register),
    path('register_form/', register_form),
    path('logout/', logout),
]
