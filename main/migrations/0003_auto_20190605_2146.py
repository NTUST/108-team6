# Generated by Django 2.2.1 on 2019-06-05 13:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20190605_2145'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teamplayer',
            unique_together={('user', 'player')},
        ),
    ]
