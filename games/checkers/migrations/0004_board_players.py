# Generated by Django 4.2.2 on 2023-10-27 16:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("checkers", "0003_remove_board_players_alter_board_guid_boardplayers"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="players",
            field=models.ManyToManyField(
                help_text="The players of the board.",
                related_name="boards_players",
                through="checkers.BoardPlayers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Players",
            ),
        ),
    ]