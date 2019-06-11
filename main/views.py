import threading

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Case, When, Value, BooleanField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from main.models import Player, TeamPlayer
from main.utils import parse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User

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


@user_passes_test(lambda u: u.is_superuser)
def refresh_data(request):
    thread = threading.Thread(target=parse)
    thread.start()
    return HttpResponse(status=200)


def parse_query_string(parameter):
    query_string = "&".join([f"{i}={v}" for i, v in parameter.items()])
    return f"?{query_string}&"


def get_player(request, player_name):
    try:
        player = Player.objects.get(number=player_name)
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


def get_team(request):
    clubs = list(Player.objects.values_list("club", flat=True).order_by("club").distinct("club"))
    team_name = request.GET.get("team")
    if team_name:
        player_list = Player.objects.filter(club=team_name)
    else:
        player_list = Player.objects.filter(teamplayer__user_id=request.user.id)
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


def edit_team(request):
    if request.method == "GET":
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
        )
        player_list = player_list.all()[start:start + limit]
        query_string = parse_query_string(parameter=parameter)
        return render(request, "edit-team.html", locals())
    else:
        player_id = request.data["id"]
        action = request.data["action"]
        if action == "add":
            TeamPlayer.objects.create(user_id=request.user.id, player_id=player_id)
        else:
            TeamPlayer.objects.filter(user_id=request.user.id, player_id=player_id).delete()
        return JsonResponse(data={}, status=200)

def register(request):
	return render(request, "register.html")

def register_form(request):
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username,email,password)
	if user:
		return redirect('/login',locals())
	else:
		return redirect('/signup',locals())

def login_form(request):

	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		login_name=request.POST['username'].strip()
		login_password=request.POST['password']
		print(login_name, login_password)
		user = authenticate(username=login_name, password=login_password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				messages.add_message(request, messages.SUCCESS, '成功登入了')
				# print('ya')
				return redirect('../')
			else:
				messages.add_message(request, messages.WARNING, '帳號尚未啟用')
		else:
			messages.add_message(request, messages.WARNING, '登入失敗')
	else:
		messages.add_message(request, messages.INFO,'請檢查輸入的欄位內容')

	return render(request, "login.html")

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功登出了")
    return redirect('/')