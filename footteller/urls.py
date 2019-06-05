from django.contrib import admin
from django.urls import path
from analysis.views import predict,predict_result
from main.views import index, players, refresh_data, get_player


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('players', players, name="base"),
    path('predict/', predict, name="predict"),
    path('analysis_form/', predict_result),
    path('players', players, name="players"),
    path('players/<str:player_name>', get_player, name="player"),
    path('refresh_data', refresh_data, name="refresh_data"),
]
