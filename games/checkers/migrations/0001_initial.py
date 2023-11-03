# Generated by Django 4.2.6 on 2023-11-03 21:07

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                (
                    "guid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="The unique identifier of the board.",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="GUID",
                    ),
                ),
                (
                    "grid",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.IntegerField(blank=True, null=True),
                            blank=True,
                            null=True,
                            size=None,
                        ),
                        blank=True,
                        default=list,
                        help_text="The grid of the board.",
                        null=True,
                        size=None,
                        verbose_name="Grid",
                    ),
                ),
                (
                    "length",
                    models.IntegerField(
                        choices=[(8, "Eight"), (10, "Ten")],
                        default=8,
                        help_text="The length of the board.",
                        verbose_name="Length",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date and time when the board was created.",
                        verbose_name="Created at",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date and time when the board was updated.",
                        verbose_name="Updated at",
                    ),
                ),
                (
                    "is_ended",
                    models.BooleanField(
                        default=False,
                        help_text="The status of the game.",
                        verbose_name="Is ended",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="The status of the board.",
                        verbose_name="Is active",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        help_text="The owner of the board.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="boards_owner",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Checkers board",
                "verbose_name_plural": "Checkers boards",
                "db_table": "checkers_boards",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="Histories",
            fields=[
                (
                    "guid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="The unique identifier of the history.",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="GUID",
                    ),
                ),
                (
                    "grid_changes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.IntegerField(), size=2
                        ),
                        help_text="Move points of the history.",
                        null=True,
                        size=None,
                        verbose_name="Grid changes",
                    ),
                ),
                (
                    "taken_points",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.IntegerField(), size=2
                        ),
                        blank=True,
                        help_text="The taken points of the history.",
                        null=True,
                        size=None,
                        verbose_name="Taken points",
                    ),
                ),
                (
                    "played_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date and time when the history was created.",
                        verbose_name="Created at",
                    ),
                ),
                (
                    "board",
                    models.ForeignKey(
                        help_text="The board of the history.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="histories",
                        to="checkers.board",
                        verbose_name="Board",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        help_text="The player of the history.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="histories",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Player",
                    ),
                ),
            ],
            options={
                "verbose_name": "Checkers history",
                "verbose_name_plural": "Checkers histories",
                "db_table": "checkers_histories",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="BoardPlayers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "stone_type",
                    models.PositiveSmallIntegerField(
                        choices=[(2, "White"), (3, "Black")], default=2
                    ),
                ),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="checkers.board"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("board", "stone_type")},
            },
        ),
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
        migrations.AddField(
            model_name="board",
            name="queue",
            field=models.ForeignKey(
                blank=True,
                help_text="The queue of the board.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="boards_queue",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Queue",
            ),
        ),
        migrations.AddField(
            model_name="board",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                help_text="The winner of the board.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="boards_winner",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Winner",
            ),
        ),
    ]
