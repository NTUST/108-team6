# Generated by Django 2.2.1 on 2019-05-25 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=1024)),
                ('age', models.IntegerField()),
                ('photo', models.URLField(null=True)),
                ('nationality', models.CharField(max_length=512)),
                ('nationality_flag', models.URLField(null=True)),
                ('overall', models.IntegerField()),
                ('potential', models.IntegerField()),
                ('club', models.CharField(max_length=512)),
                ('club_logo', models.URLField(null=True)),
                ('value', models.IntegerField()),
                ('wage', models.IntegerField()),
                ('special', models.IntegerField()),
                ('preferred_foot', models.CharField(max_length=64)),
                ('international_reputation', models.IntegerField()),
                ('weak_foot', models.IntegerField()),
                ('skill_moves', models.IntegerField()),
                ('work_rate', models.CharField(max_length=512)),
                ('body_type', models.CharField(max_length=512)),
                ('position', models.CharField(max_length=512)),
                ('jersey_number', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('ls', models.IntegerField()),
                ('st', models.IntegerField()),
                ('rs', models.IntegerField()),
                ('lw', models.IntegerField()),
                ('lf', models.IntegerField()),
                ('cf', models.IntegerField()),
                ('rf', models.IntegerField()),
                ('rw', models.IntegerField()),
                ('lam', models.IntegerField()),
                ('cam', models.IntegerField()),
                ('ram', models.IntegerField()),
                ('lm', models.IntegerField()),
                ('lcm', models.IntegerField()),
                ('cm', models.IntegerField()),
                ('rcm', models.IntegerField()),
                ('rm', models.IntegerField()),
                ('lwb', models.IntegerField()),
                ('ldm', models.IntegerField()),
                ('cdm', models.IntegerField()),
                ('rdm', models.IntegerField()),
                ('rwb', models.IntegerField()),
                ('lb', models.IntegerField()),
                ('lcb', models.IntegerField()),
                ('cb', models.IntegerField()),
                ('rcb', models.IntegerField()),
                ('rb', models.IntegerField()),
                ('crossing', models.IntegerField()),
                ('finishing', models.IntegerField()),
                ('heading_accuracy', models.IntegerField()),
                ('short_passing', models.IntegerField()),
                ('volleys', models.IntegerField()),
                ('dribbling', models.IntegerField()),
                ('curve', models.IntegerField()),
                ('fk_accuracy', models.IntegerField()),
                ('long_passing', models.IntegerField()),
                ('ball_control', models.IntegerField()),
                ('acceleration', models.IntegerField()),
                ('sprint_speed', models.IntegerField()),
                ('agility', models.IntegerField()),
                ('reactions', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('shot_power', models.IntegerField()),
                ('jumping', models.IntegerField()),
                ('stamina', models.IntegerField()),
                ('strength', models.IntegerField()),
                ('long_shots', models.IntegerField()),
                ('aggression', models.IntegerField()),
                ('interceptions', models.IntegerField()),
                ('positioning', models.IntegerField()),
                ('vision', models.IntegerField()),
                ('penalties', models.IntegerField()),
                ('composure', models.IntegerField()),
                ('marking', models.IntegerField()),
                ('standing_tackle', models.IntegerField()),
                ('sliding_tackle', models.IntegerField()),
                ('gk_diving', models.IntegerField()),
                ('gk_handling', models.IntegerField()),
                ('gk_kicking', models.IntegerField()),
                ('gk_positioning', models.IntegerField()),
                ('gk_reflexes', models.IntegerField()),
                ('release_clause', models.IntegerField()),
            ],
        ),
    ]