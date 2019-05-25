from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def players(request):
    return render(request, "players.html")
