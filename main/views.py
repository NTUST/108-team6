import threading

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from main.models import Player
from main.utils import parse


def index(request):
    return render(request, "index.html")


@require_http_methods(["GET"])
def players(request):
    page = int(request.GET.get('page', 1))
    page = page if page > 1 else 1
    limit = int(request.GET.get('limit', 20))
    limit = limit if 0 < limit < 50 else 20
    start = (page - 1) * limit
    player_list = Player.objects.all()[start:start + limit]
    return render(request, "players.html", locals())


@user_passes_test(lambda u: u.is_superuser)
def refresh_data(request):
    thread = threading.Thread(target=parse)
    thread.start()
    return HttpResponse(status=200)


def get_player(request, player_name):
    try:
        player = Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        player = None

    return render(request, "player.html", locals())
