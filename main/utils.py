import pandas
from django.db import connection


def to_string(x):
    if isinstance(x, float):
        x = int(x)
    return x


def parse(filename="pre.csv"):
    data = pandas.read_csv(filename)
    prefix = 'INSERT INTO main_player ("number", "name", "age", "photo", "nationality", "nationality_flag", "overall", "potential", "club", "club_logo", "value", "wage", "special", "preferred_foot", "international_reputation", "weak_foot", "skill_moves", "work_rate", "body_type", "position", "jersey_number", "height", "weight", "ls", "st", "rs", "lw", "lf", "cf", "rf", "rw", "lam", "cam", "ram", "lm", "lcm", "cm", "rcm", "rm", "lwb", "ldm", "cdm", "rdm", "rwb", "lb", "lcb", "cb", "rcb", "rb", "crossing", "finishing", "heading_accuracy", "short_passing", "volleys", "dribbling", "curve", "fk_accuracy", "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", "reactions", "balance", "shot_power", "jumping", "stamina", "strength", "long_shots", "aggression", "interceptions", "positioning", "vision", "penalties", "composure", "marking", "standing_tackle", "sliding_tackle", "gk_diving", "gk_handling", "gk_kicking", "gk_positioning", "gk_reflexes", "release_clause") VALUES ({});\n'
    with connection.cursor() as cursor:
        for i in data.values:
            cursor.execute(
                prefix.format(str(list(map(to_string, i.tolist())))[1:-1].replace('"', "'")))


def parse_query_string(parameter):
    query_string = "&".join([f"{i}={v}" for i, v in parameter.items()])
    return f"?{query_string}&"
