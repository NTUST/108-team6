# Generated by Django 2.2.1 on 2019-06-11 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190605_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='club',
            field=models.CharField(db_index=True, max_length=512),
        ),
    ]
