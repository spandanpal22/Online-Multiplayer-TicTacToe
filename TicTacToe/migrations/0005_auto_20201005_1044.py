# Generated by Django 3.1.1 on 2020-10-05 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicTacToe', '0004_auto_20201002_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='winner',
            field=models.CharField(blank=True, max_length=1000, null=True, unique=True),
        ),
    ]
