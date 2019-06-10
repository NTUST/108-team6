import threading

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Case, When, Value, BooleanField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from main.models import Player, TeamPlayer
from main.utils import parse


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


def get_teams(request):
    clubs = [
        "Boavista FC", "Fenerbahçe SK", "Botafogo", "Vitesse", "Eintracht Frankfurt", "Montpellier HSC",
        "Minnesota United FC", "Kawasaki Frontale", "DSC Arminia Bielefeld", "Aarhus GF", "Ajax", "Crystal Palace",
        "Dinamo Zagreb", "Valencia CF", "US Cremonese", "Heracles Almelo", "CD Everton de Viña del Mar",
        "Club Atlético Lanús", "FK Bodø/Glimt", "RCD Mallorca", "Shrewsbury", "Columbus Crew SC", "Shamrock Rovers",
        "Arka Gdynia", "Dundalk", "Real Salt Lake", "Middlesbrough", "Manchester City", "BB Erzurumspor",
        "Vålerenga Fotball", "Málaga CF", "Chicago Fire", "KAS Eupen", "Vélez Sarsfield", "Red Star FC",
        "SV Werder Bremen", "Stevenage", "Incheon United FC", "Nagoya Grampus", "Wisła Płock", "Odds BK",
        "Accrington Stanley", "Universidad Católica", "AIK", "Hamburger SV", "Crotone", "AS Nancy Lorraine",
        "ESTAC Troyes", "Arsenal", "Henan Jianye FC", "Pohang Steelers", "Kilmarnock", "Genoa", "Puebla FC",
        "Boyacá Chicó FC", "Molde FK", "Viktoria Plzeň", "Al Shabab", "Santos", "Club América", "AZ Alkmaar",
        "Southampton", "Vissel Kobe", "SC Paderborn 07", "Club Necaxa", "Grasshopper Club Zürich", "Olympiacos CFP",
        "Tianjin TEDA FC", "Fiorentina", "Chelsea", "Lech Poznań", "Bournemouth", "FC Nantes", "Aston Villa",
        "Feyenoord", "Birmingham City", "FC Admira Wacker Mödling", "PAOK", "Brentford", "Gangwon FC",
        "Akhisar Belediyespor", "Stade Rennais FC", "Willem II", "Swansea City", "Getafe CF",
        "América FC (Minas Gerais)", "New York Red Bulls", "SC Heerenveen", "FK Austria Wien", "VfL Osnabrück",
        "Notts County", "Shakhtar Donetsk", "Guangzhou Evergrande Taobao FC", "Kaizer Chiefs", "Paraná",
        "Deportes Tolima", "Forest Green Rovers", "Coventry City", "Sivasspor", "Derry City", "SD Eibar", "Port Vale",
        "Beijing Renhe FC", "Vancouver Whitecaps FC", "San Martin de Tucumán", "Barnsley", "BK Häcken",
        "Medipol Başakşehir FK", "SK Rapid Wien", "Monarcas Morelia", "Portsmouth", "1. FC Nürnberg",
        "Milton Keynes Dons", "Shonan Bellmare", "Zagłębie Sosnowiec", "AFC Wimbledon", "1. FC Heidenheim 1846",
        "Torino", "Vitória", "Rayo Vallecano", "SV Mattersburg", "Sporting CP", "VfB Stuttgart", "Ascoli", "Pachuca",
        "Deportes Iquique", "Cosenza", "Cittadella", "Aalborg BK", "Miedź Legnica", "Deportivo Cali", "FC Metz",
        "América de Cali", "FC Carl Zeiss Jena", "Club Brugge KV", "Bologna", "FC Dallas", "FC Energie Cottbus",
        "Melbourne City FC", "Levante UD", "TSG 1899 Hoffenheim", "Kasimpaşa SK", "UD Almería", "SCR Altach",
        "Curicó Unido", "Leicester City", "Al Fayha", "Randers FC", "Trelleborgs FF", "Yeovil Town", "Watford",
        "Millonarios FC", "Ettifaq FC", "Wolfsberger AC", "US Orléans Loiret Football", "Newcastle Jets", "Motherwell",
        "Atlético Tucumán", "Gimnasia y Esgrima La Plata", "SK Brann", "Kashima Antlers", "Sevilla FC",
        "RC Strasbourg Alsace", "FC Emmen", "KAA Gent", "Malmö FF", "Stade Brestois 29", "Guangzhou R&F; FC",
        "CD Palestino", "La Berrichonne de Châteauroux", "Beijing Sinobo Guoan FC", "Djurgårdens IF", "FC Lugano",
        "Manchester United", "Rotherham United", "Parma", "San Lorenzo de Almagro", "Cheltenham Town", "FC Luzern",
        "Galatasaray SK", "Milan", "IFK Norrköping", "Itagüí Leones FC", "Albacete BP", "Luton Town", "Grêmio",
        "Rionegro Águilas", "Gimnàstic de Tarragona", "Vejle Boldklub", "Gamba Osaka", "Rochdale",
        "Club Atlético Banfield", "Paris Saint-Germain", "Leeds United", "Kristiansund BK", "Club Tijuana",
        "Ceará Sporting Club", "Al Qadisiyah", "Oldham Athletic", "Crawley Town"
    ]
    return render("teams.html",locals())


def get_team_players(request):
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
