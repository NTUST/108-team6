# Generated by Django 2.2.1 on 2019-06-11 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190612_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
