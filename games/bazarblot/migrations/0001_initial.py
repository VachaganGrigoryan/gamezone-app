# Generated by Django 4.2.2 on 2023-10-27 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Card",
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
                    "suit",
                    models.CharField(
                        choices=[
                            ("Hearts", "Hearts"),
                            ("Diamonds", "Diamonds"),
                            ("Clubs", "Clubs"),
                            ("Spades", "Spades"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("10", "10"),
                            ("K", "K"),
                            ("Q", "Q"),
                            ("J", "J"),
                            ("9", "9"),
                            ("8", "8"),
                            ("7", "7"),
                        ],
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Game",
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
                ("name", models.CharField(max_length=100)),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("is_finished", models.BooleanField(default=False)),
                (
                    "winning_team",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("current_round", models.IntegerField(default=1)),
                ("max_points", models.IntegerField(default=301)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
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
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Round",
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
                    "trump_suit",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Hearts", "Hearts"),
                            ("Diamonds", "Diamonds"),
                            ("Clubs", "Clubs"),
                            ("Spades", "Spades"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("round_number", models.IntegerField()),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "current_player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="round_current_player",
                        to="bazarblot.player",
                    ),
                ),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="round_dealer",
                        to="bazarblot.player",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bazarblot.game"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trick",
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
                    "card_played",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bazarblot.card"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bazarblot.player",
                    ),
                ),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bazarblot.round",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Score",
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
                ("points", models.IntegerField()),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bazarblot.game"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bazarblot.player",
                    ),
                ),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bazarblot.round",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Quanch",
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
                    "trump_suit",
                    models.CharField(
                        choices=[
                            ("Hearts", "Hearts"),
                            ("Diamonds", "Diamonds"),
                            ("Clubs", "Clubs"),
                            ("Spades", "Spades"),
                        ],
                        max_length=10,
                    ),
                ),
                ("x_points", models.IntegerField()),
                ("y_points", models.IntegerField()),
                ("is_successful", models.BooleanField()),
                (
                    "quanch_type",
                    models.CharField(
                        choices=[
                            ("Quanch", "Quanch"),
                            ("Sharpened Quanch", "Sharpened Quanch"),
                        ],
                        max_length=20,
                    ),
                ),
                ("sharpened_x_points", models.IntegerField(blank=True, null=True)),
                ("sharpened_y_points", models.IntegerField(blank=True, null=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bazarblot.game"
                    ),
                ),
                (
                    "player_quanching",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quanch_player_quanching",
                        to="bazarblot.player",
                    ),
                ),
                (
                    "player_sharpening",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quanch_player_sharpening",
                        to="bazarblot.player",
                    ),
                ),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bazarblot.round",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Combination",
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
                ("combination_type", models.CharField(max_length=10)),
                ("is_sharpened", models.BooleanField(default=False)),
                (
                    "cards_in_combination",
                    models.ManyToManyField(
                        related_name="combinations_in_cards", to="bazarblot.card"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bazarblot.player",
                    ),
                ),
                (
                    "trump_card",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="combination_trump_card",
                        to="bazarblot.card",
                    ),
                ),
            ],
        ),
    ]
