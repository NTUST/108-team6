import threading

import numpy
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, BooleanField, Avg
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from analysis.views import predict_value
from main.constants import CLUBS
from main.models import Player, TeamPlayer
from main.utils import parse, parse_query_string


@user_passes_test(lambda u: u.is_superuser)
def refresh_data(request):
    thread = threading.Thread(target=parse)
    thread.start()
    return redirect(to='index')


@require_http_methods(["GET"])
def index(request):
    return render(request, "index.html")


@require_http_methods(["GET"])
def players(request):
    parameter = {}
    page = int(request.GET.get('page', 1))
    page = page if page > 1 else 1
    limit = int(request.GET.get('limit', 20))
    limit = limit if 0 < limit < 50 else 20
    start = (page - 1) * limit

    player_list = Player.objects.filter()
    order = request.GET.get("order")
    order_by = request.GET.get("order_by")
    search_name = request.GET.get("search")
    if search_name:
        parameter["search"] = search_name
        player_list = player_list.filter(name__contains=search_name)
    if order and order_by:
        order_column = order_by
        if order not in ["asc", "desc"]:
            order = "asc"
        if order == "desc":
            order_column = f"-{order_column}"
        player_list = player_list.order_by(order_column)
    player_list = player_list.all()[start:start + limit]
    query_string = parse_query_string(parameter=parameter)
    title = 'Players'
    return render(request, "players.html", locals())


@require_http_methods(["GET"])
def player(request, player_number):
    try:
        player = Player.objects.get(id=player_number)
    except Player.DoesNotExist:
        player = None

    if player is not None:
        atk = round(
            (player.crossing + player.finishing + player.heading_accuracy +
             player.short_passing + player.volleys) / 5)
        skill = round(
            (player.dribbling + player.curve + player.fk_accuracy + player.long_passing + player.ball_control) / 5)
        move = round(
            (player.acceleration + player.sprint_speed + player.agility +
             player.reactions + player.balance) / 5)
        power = round((player.shot_power + player.jumping + player.stamina +
                       player.strength + player.long_shots) / 5)
        mental = round(
            (player.aggression + player.interceptions + player.positioning +
             player.vision + player.penalties) / 5)
        defend = round(
            (player.marking + player.standing_tackle + player.sliding_tackle) / 3)
        goal = round(
            (player.gk_diving + player.gk_handling + player.gk_kicking +
             player.gk_positioning + player.gk_reflexes) / 5)

        data = [atk, skill, move, power, mental, defend, goal]
    title = 'Players'
    return render(request, "player.html", locals())


@require_http_methods(["GET"])
def team(request):
    title = "Team"
    clubs = CLUBS
    team_name = request.GET.get("team")
    if not request.user.id:
        rating = potential = value = wage = 0
        player_list = []
    else:
        if not team_name or team_name == "MyTeam":
            player_list = Player.objects.filter(teamplayer__user_id=request.user.id)
        else:
            player_list = Player.objects.filter(club=team_name)
        result = player_list.aggregate(rating=Avg("overall"), potential=Avg("potential"), wage=Avg("wage"),
                                       value=Avg("value"))
        rating = int(result["rating"] if result["rating"] is not None else 0)
        potential = int(result["potential"] if result["potential"] is not None else 0)
        value = result["value"] if result["value"] is not None else 0
        wage = result["wage"] if result["wage"] is not None else 0
    value = "{:.2f}M".format(value / 1000) if value > 1000 else f"{value}k"
    wage = "{:.2f}M".format(wage / 1000) if wage > 1000 else f"{wage}k"
    order = request.GET.get("order")
    order_by = request.GET.get("order_by")
    if order and order_by:
        order_column = order_by
        if order not in ["asc", "desc"]:
            order = "asc"
        if order == "desc":
            order_column = f"-{order_column}"
        player_list = player_list.order_by(order_column)
    return render(request, "team.html", locals())


@require_http_methods(["POST", "GET"])
@login_required
def edit_team(request):
    def get_method(request):
        parameter = {}
        page = int(request.GET.get('page', 1))
        page = page if page > 1 else 1
        limit = int(request.GET.get('limit', 20))
        limit = limit if 0 < limit < 50 else 20
        start = (page - 1) * limit

        player_list = Player.objects.filter()
        order = request.GET.get("order")
        order_by = request.GET.get("order_by")
        search_name = request.GET.get("search")
        if search_name:
            parameter["search"] = search_name
            player_list = player_list.filter(name__contains=search_name)
        if order and order_by:
            order_column = order_by
            if order not in ["asc", "desc"]:
                order = "asc"
            if order == "desc":
                order_column = f"-{order_column}"
            player_list = player_list.order_by(order_column)
        player_list = player_list.annotate(
            is_chosen=Case(
                When(teamplayer__isnull=True, then=False),
                default=Value(True),
                output_field=BooleanField(),
            )
        ).order_by("-is_chosen")
        player_list = player_list.all()[start:start + limit]
        query_string = parse_query_string(parameter=parameter)
        return render(request, "edit-team.html", locals())

    if request.method == "GET":
        return get_method(request)
    else:
        remove_ids = request.POST.get("unchecked_ids")
        if remove_ids:
            remove_ids = list(map(lambda x: int(x), remove_ids.split(',')))
            TeamPlayer.objects.filter(player_id__in=remove_ids, user_id=request.user.id).delete()
        add_ids = request.POST.get("checked_ids")
        if add_ids:
            add_ids = list(map(lambda x: int(x), add_ids.split(',')))
            TeamPlayer.objects.bulk_create([
                TeamPlayer(user_id=request.user.id, player_id=i) for i in add_ids
            ])
        return get_method(request)


@require_http_methods(["POST", "GET"])
@login_required
def create_player(request):
    title = "Create"
    if request.method == "GET":
        positions = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW', 'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM',
                     'RM',
                     'LWB', 'LDM', 'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']
        rating = [
            ['', 'LS', 'ST', 'RS', ''],
            ['LW', 'LF', 'CF', 'RF', 'RW'],
            ['', 'LAM', 'CAM', 'RAM', ''],
            ['LM', 'LCM', 'CM', 'RCM', 'RM'],
            ['LWB', 'LDM', 'CDM', 'RDM', 'RWB'],
            ['LB', 'LCB', 'CB', 'RCB', 'RB']
        ]

        attributes = {
            'Attacking': ['Crossing', 'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys'],
            'Skill': ['Dribbling', 'Curve', 'FK Accuracy', 'Long Passing', 'Ball Control'],
            'Movement': ['Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance'],
            'Power': ['Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots'],
            'Mentality': ['Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure'],
            'Defending': ['Marking', 'Standing Tackle', 'Sliding Tackle'],
            'Goalkeeping': ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes'],
        }

        preferred_foot = ['right', 'left']
        range_5 = ['1', '2', '3', '4', '5']
        work_rate = ['High/ High', 'High/ Low', 'High/ Medium', 'Low/ High', 'Low/ Low', 'Low/ Medium', 'Medium/ High',
                     'Medium/ Low', 'Medium/ Medium']
        body_type = ['C. Ronaldo', 'Courtois', 'Lean', 'Messi', 'Neymar', 'Normal', 'Stocky']

        return render(request, "create_player.html", locals())
    else:
        player = Player()
        for i in request.POST:
            key = i.lower().replace(" ", "_")
            if hasattr(player, key):
                setattr(player, key, request.POST[i])
        player.overall = request.POST.get("rating")
        player.special = 1625
        player.nationality = "Taiwan"
        player.nationality_flag = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Flag_of_the_Republic_of_China.svg/188px-Flag_of_the_Republic_of_China.svg.png"
        player.club = request.user.username
        player.club_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/NTUST-Emblem.png/220px-NTUST-Emblem.png"
        player.creator_id = request.user.id
        arr_list = ['age', 'rating', 'potential', 'Special', 'Acceleration', 'Aggression', 'Agility', 'Balance',
                    'Ball Control', 'Composure', 'Crossing', 'Curve', 'Dribbling', 'Finishing', 'Free Kick Accuracy',
                    'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy',
                    'Interceptions', 'Jumping', 'Long Passing', 'Long Shots', 'Marking', 'Penalties', 'Positioning',
                    'Reactions', 'Short Passing', 'Shot Power', 'Sliding Tackle', 'Sprint Speed', 'Stamina',
                    'Standing Tackle', 'Strength', 'Vision', 'Volleys']
        prefer_list = ['CAM', 'CB', 'CDM', 'CF', 'CM', 'GK', 'LB', 'LM', 'LW', 'RB', 'RM', 'RW', 'RWB', 'ST', 'LWB']
        inputs = []
        for arr in arr_list:
            if arr not in request.POST:
                print(arr)
                inputs.append(80)
            else:
                inputs.append(int(request.POST.get(arr)))

        prefers = [] if request.POST.getlist('prefer[]') is None else request.POST.getlist('prefer[]')
        for prefer in prefer_list:
            if prefer in prefers:
                inputs.append(1)
            else:
                inputs.append(0)
        player.release_clause = player.wage = player.value = predict_value(numpy.array(inputs)) / 1000
        player.save()
        TeamPlayer.objects.create(user_id=request.user.id, player_id=player.id)
        return redirect(to="team")


@require_http_methods(["POST", "GET"])
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    if user:
        return redirect('/login', locals())
    else:
        return render(request, "register.html")


@require_http_methods(["POST", "GET"])
def login(request):
    if request.user.is_authenticated:
        return redirect(to='index')
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            auth.login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect(to="index")
    return render(request, "login.html")


@require_http_methods(["GET"])
def logout(request):
    auth.logout(request)
    return redirect(to='index')

def donate(request):
    title = 'Donate'
    return render(request, "donate.html", locals())
